from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import logging
import os
import sys

# Adicionar path para importar nfe_config
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

try:
    from modules.nfe.nfe_config import CONFIG_NFE
except ImportError:
    print("❌ Módulo nfe_config não encontrado. Usando variáveis de ambiente como fallback.")
    from dotenv import load_dotenv
    load_dotenv()

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

def get_credenciais_nfe():
    """
    Obtém as credenciais do NFE do nfe_config.py ou do .env como fallback
    """
    try:
        # Tentar obter do nfe_config primeiro
        if 'CONFIG_NFE' in globals():
            return {
                'url': CONFIG_NFE['url_nfe'],
                'usuario': CONFIG_NFE['usuario'],
                'senha': CONFIG_NFE['senha'],
                'ir': CONFIG_NFE['ir']
            }
    except:
        pass
    
    # Fallback para variáveis de ambiente
    from dotenv import load_dotenv
    load_dotenv()
    
    return {
        'url': os.getenv('URL_NFE'),
        'usuario': os.getenv('NFE_USUARIO'),
        'senha': os.getenv('NFE_SENHA')
    }

def fazer_login_nfe():
    """
    Função principal para fazer login no sistema de NFe
    
    Returns:
        driver: Instância do WebDriver se login bem-sucedido, None caso contrário
    """
    print("🔐 FAZENDO LOGIN NO SISTEMA DE NFE")
    print("=" * 50)
    
    # Obter credenciais
    credenciais = get_credenciais_nfe()
    
    URL_NFE = credenciais['url']
    NFE_USUARIO = credenciais['usuario']
    NFE_SENHA = credenciais['senha']
    
    # Verificar se variáveis foram carregadas
    if not all([URL_NFE, NFE_USUARIO, NFE_SENHA]):
        print("❌ Credenciais NFE não configuradas corretamente")
        print("   Verifique o arquivo .env ou nfe_config.py")
        return None
    
    print(f"🌐 URL: {URL_NFE}")
    print(f"👤 Usuário: {NFE_USUARIO}")
    print(f"🔑 Senha: {'*' * len(NFE_SENHA) if NFE_SENHA else 'Não configurada'}")
    
    # Inicializar driver
    driver = webdriver.Chrome()
    driver.maximize_window()
    
    try:
        print(f"🌐 Acessando sistema de NFe...")
        driver.get(URL_NFE)
        
        # Aguardar página carregar
        time.sleep(2)
        
        # Preencher usuário
        print(f"👤 Preenchendo usuário...")
        usuario_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "txtLogin"))
        )
        usuario_input.clear()
        usuario_input.send_keys(NFE_USUARIO)
        
        # Aguardar teclado virtual carregar
        time.sleep(3)
        
        print("⌨️ Teclado virtual detectado - necessário interação manual")
        print("⚠️ Por favor, insira a senha manualmente no teclado virtual")
        time.sleep(1)
        input("Pressione Enter após completar o login manual...")
        print("⚠️ Por favor, volte para o site do sistema NFE em até 10 segundos...")
        time.sleep(10)
        # Verificar se login foi bem-sucedido
        try:
            # Verificar se elemento pós-login está presente
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "txtCae"))
            )
            print("✅ Login realizado com sucesso!")
            return driver
            
        except TimeoutException:
            print("❌ Possível falha no login - elemento pós-login não encontrado")
            print("⚠️ Verifique se o login foi feito manualmente e continue")
            return driver
            
    except Exception as e:
        print(f"❌ Erro durante o login: {str(e)}")
        driver.quit()
        return None

def verificar_login_nfe(driver):
    """
    Verifica se o login foi bem sucedido no sistema NFE
    """
    if not driver:
        return False
    
    try:
        # Verificar vários elementos que indicam login bem-sucedido
        elementos_validacao = [
            (By.ID, "txtCae")
        ]
        
        for by, value in elementos_validacao:
            try:
                if driver.find_elements(by, value):
                    print(f"✅ Login verificado - elemento encontrado: {value}")
                    return True
            except:
                continue
        
        # Verificar pela URL (se não contém 'login')
        if "login" not in driver.current_url.lower():
            print("✅ Login verificado - URL não contém 'login'")
            return True
        
        print("❌ Login não verificado - nenhum elemento de validação encontrado")
        return False
        
    except Exception as e:
        print(f"❌ Erro ao verificar login: {str(e)}")
        return False

def testar_coordenadas_nfe():
    """
    Função para testar coordenadas e elementos da página
    """
    print("🎯 TESTANDO COORDENADAS E ELEMENTOS")
    print("=" * 50)
    
    # Obter URL das credenciais
    credenciais = get_credenciais_nfe()
    URL_NFE = credenciais['url']
    
    # Verificar se URL foi carregada
    if not URL_NFE:
        print("❌ URL_NFE não configurada")
        return False
    
    driver = webdriver.Chrome()
    
    try:
        driver.get(URL_NFE)
        time.sleep(3)
        
        print("📋 Elementos encontrados na página:")
        print("-" * 30)
        
        # Procurar elementos comuns
        elementos_testar = [
            "txtLogin", "txtSenha", "btnLogin", 
            "input[type='button']", "button", "div[onclick]"
        ]
        
        for seletor in elementos_testar:
            try:
                if seletor in ["txtLogin", "txtSenha", "btnLogin"]:
                    elementos = driver.find_elements(By.ID, seletor)
                else:
                    elementos = driver.find_elements(By.CSS_SELECTOR, seletor)
                
                if elementos:
                    print(f"✅ {seletor}: {len(elementos)} elemento(s) encontrado(s)")
                    for i, elemento in enumerate(elementos[:3]):
                        texto = elemento.text or elemento.get_attribute("value") or elemento.get_attribute("innerText")
                        print(f"   {i+1}. Texto: '{texto[:50]}'")
                else:
                    print(f"❌ {seletor}: Nenhum elemento encontrado")
                    
            except Exception as e:
                print(f"⚠️ Erro ao buscar {seletor}: {str(e)}")
                
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste de coordenadas: {str(e)}")
        return False
    finally:
        driver.quit()

def fazer_logout_nfe(driver):
    """
    Faz logout do sistema NFE
    """
    if not driver:
        return
    
    try:
        # Tentar encontrar e clicar no botão de logout
        elementos_logout = [
            (By.ID, "btnSair"),
            (By.ID, "btnLogout"),
            (By.XPATH, "//a[contains(text(), 'Sair') or contains(text(), 'Logout')]"),
            (By.CLASS_NAME, "logout-button")
        ]
        
        for by, value in elementos_logout:
            try:
                logout_btn = driver.find_element(by, value)
                logout_btn.click()
                print("✅ Logout realizado com sucesso")
                time.sleep(2)
                return
            except:
                continue
        
        print("⚠️ Botão de logout não encontrado")
        
    except Exception as e:
        print(f"❌ Erro ao fazer logout: {str(e)}")

# Exemplo de uso
if __name__ == "__main__":
    print("🧪 Teste do módulo de login NFE")
    print("=" * 50)
    
    # Testar obtenção de credenciais
    credenciais = get_credenciais_nfe()
    print("Credenciais obtidas:")
    for key, value in credenciais.items():
        if key == 'senha':
            value = '*' * len(value) if value else 'None'
        print(f"  {key}: {value}")
    
    # Testar login
    driver = fazer_login_nfe()
    if driver:
        if verificar_login_nfe(driver):
            print("✅ Teste de login completo e verificado!")
        else:
            print("⚠️ Login realizado mas não verificado")
        
        # Fazer logout e fechar
        fazer_logout_nfe(driver)
        driver.quit()
    else:
        print("❌ Falha no teste de login")