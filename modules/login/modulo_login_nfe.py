from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import logging
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

# Constantes das variáveis de ambiente
URL_NFE = os.getenv('URL_NFE')
NFE_USUARIO = os.getenv('NFE_USUARIO')
NFE_SENHA = os.getenv('NFE_SENHA')

def fazer_login_nfe():
    """
    Função principal para fazer login no sistema de NFe
    
    Returns:
        driver: Instância do WebDriver se login bem-sucedido, None caso contrário
    """
    print("🔐 FAZENDO LOGIN NO SISTEMA DE NFE")
    print("=" * 50)
    
    # Verificar se variáveis de ambiente foram carregadas
    if not all([URL_NFE, NFE_USUARIO, NFE_SENHA]):
        print("❌ Variáveis de ambiente não configuradas corretamente")
        print("   Verifique o arquivo .env")
        return None
    
    # Inicializar driver
    driver = webdriver.Chrome()
    driver.maximize_window()
    
    try:
        print(f"🌐 Acessando sistema de NFe: {URL_NFE}")
        driver.get(URL_NFE)
        
        # Aguardar página carregar
        time.sleep(2)
        
        # Preencher usuário
        print(f"👤 Preenchendo usuário: {NFE_USUARIO}")
        usuario_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "txtLogin"))
        )
        usuario_input.clear()
        usuario_input.send_keys(NFE_USUARIO)
        
        # Aguardar teclado virtual carregar
        time.sleep(3)
        
        print("⌨️ Teclado virtual detectado - necessário interação manual")
        print("⚠️ Por favor, insira a senha manualmente no teclado virtual")
        print("⏳ Aguardando 60 segundos para login manual...")
        
        # Aguardar tempo para inserção manual da senha
        time.sleep(60)
        
        # Verificar se login foi bem-sucedido
        try:
            # Verificar se elemento pós-login está presente
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "ctl00_Conteudo_UpdatePanel1"))
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

def testar_coordenadas_nfe():
    """
    Função para testar coordenadas e elementos da página
    """
    print("🎯 TESTANDO COORDENADAS E ELEMENTOS")
    print("=" * 50)
    
    # Verificar se URL foi carregada
    if not URL_NFE:
        print("❌ URL_NFE não configurada no arquivo .env")
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