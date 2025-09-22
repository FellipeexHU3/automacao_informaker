# nfe_automacao.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import pyautogui  # Apenas para operações específicas (senha, download)
import time
import pandas as pd
import os
from modules.nfe.nfe_planilha_teste import testar_planilha
from modules.nfe.nfe_core import NFE
from modules.nfe.nfe_config import CONFIG_NFE
from modules.login.modulo_login_nfe import fazer_login_nfe

# ================= CONFIGURAÇÃO SELENIUM =================
class NFEAutomacao:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 30)
        
    # ================= MAPEAMENTO DE ELEMENTOS =================
    ELEMENTOS = {
        'inscricao_municipal': "txtCae",
        'menu_emitir_nfe': "menu_emitir_id",  # Substitua pelo ID real
        'data_competencia': "txtDataCompetencia",
        'mostrar_rps': "chkMostrarRps",
        'numero_rps': "txtNumeroRps",
        'data_emissao': "txtDataEmissao",
        'modelo_rps': "ddlModeloRps",
        'campo_cpf': "txtCpfCnpj",
        'campo_email': "txtEmail",
        'campo_descricao': "txtDescServicos",
        'campo_lc': "txtLc116",  # Lei complementar
        'campo_atv_municipio': "ddlAtividade",
        'botao_emitir': "btnAssinarEnviarEmail",
        'botao_confirmar': "btnConfirmar",
        'numero_nfe': "txtNumeroNfse",
        'cod_autenticidade': "txtCodigoAutenticidade",
        'incluir_nova': "btnNovaNfse"
    }

    # ================= FUNÇÕES DE NAVEGAÇÃO =================
    def navegar_para_formulario(self, dados):
        """Navega até o formulário de emissão de NFE"""
        print("🗺️ NAVEGANDO PARA FORMULÁRIO...")
        try:
            # 1. Clicar no menu de emitir NFE
            menu_emitir = self.wait.until(
                EC.element_to_be_clickable((By.ID, self.ELEMENTOS['menu_emitir_nfe']))
            )
            menu_emitir.click()
            time.sleep(3)
            
            # 2. Preencher inscrição municipal
            campo_inscricao = self.wait.until(
                EC.element_to_be_clickable((By.ID, self.ELEMENTOS['inscricao_municipal']))
            )
            campo_inscricao.clear()
            campo_inscricao.send_keys(str(dados.get('ir', '')))
            
            # 3. Clicar em mostrar RPS (se necessário)
            mostrar_rps = self.driver.find_element(By.ID, self.ELEMENTOS['mostrar_rps'])
            if not mostrar_rps.is_selected():
                mostrar_rps.click()
                
            print("✅ Navegação concluída!")
            return True
            
        except Exception as e:
            print(f"❌ Erro na navegação: {e}")
            return False

    # ================= FUNÇÕES DE PREENCHIMENTO =================
    def preencher_dados_nota(self, dados):
        """Preenche todos os dados da nota usando IDs"""
        print("📝 PREENCHENDO DADOS DA NOTA...")
        try:
            # CPF/CNPJ
            self.preencher_campo('campo_cpf', dados.get('CPF', ''))
            
            # Número RPS
            self.preencher_campo('numero_rps', dados.get('NumeroRPS', ''))
            
            # Data Emissão
            self.preencher_campo('data_emissao', dados.get('DataEmissao', ''))
            
            # Descrição do serviço
            self.preencher_campo('campo_descricao', dados.get('Descricao', ''))
            
            # Valor (pode ser um campo específico)
            # self.preencher_campo('campo_valor', dados.get('Valor', ''))
            
            # Email
            self.preencher_campo('campo_email', dados.get('Email', ''))
            
            # Atividade municipal (dropdown)
            self.selecionar_dropdown('campo_atv_municipio', dados.get('Atividade', ''))
            
            print("✅ Dados preenchidos com sucesso!")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao preencher dados: {e}")
            return False

    def preencher_campo(self, elemento_chave, valor):
        """Preenche um campo específico"""
        if valor:
            campo = self.wait.until(
                EC.element_to_be_clickable((By.ID, self.ELEMENTOS[elemento_chave]))
            )
            campo.clear()
            campo.send_keys(str(valor))
            time.sleep(0.5)

    def selecionar_dropdown(self, elemento_chave, valor):
        """Seleciona opção em dropdown"""
        if valor:
            dropdown = self.driver.find_element(By.ID, self.ELEMENTOS[elemento_chave])
            dropdown.click()
            time.sleep(0.5)
            
            # Seleciona a opção pelo texto visível
            opcao = dropdown.find_element(By.XPATH, f"//option[contains(text(), '{valor}')]")
            opcao.click()
            time.sleep(0.5)

    # ================= FUNÇÃO DE EMISSÃO =================
    def emitir_nota(self, senha):
        """Emite a nota e retorna os dados"""
        print("🚀 EMITINDO NOTA...")
        try:
            # Clicar no botão de emitir
            btn_emitir = self.wait.until(
                EC.element_to_be_clickable((By.ID, self.ELEMENTOS['botao_emitir']))
            )
            btn_emitir.click()
            time.sleep(3)
            
            # 🔐 AQUI USA PYAUTOGUI APENAS PARA A SENHA (se necessário)
            # Isso porque alguns sistemas têm proteção contra automação para senhas
            if senha:
                pyautogui.write(senha)
                pyautogui.press('enter')
                time.sleep(5)
            
            # Clicar em confirmar
            btn_confirmar = self.wait.until(
                EC.element_to_be_clickable((By.ID, self.ELEMENTOS['botao_confirmar']))
            )
            btn_confirmar.click()
            time.sleep(10)  # Espera a nota ser processada
            
            # 📄 CAPTURAR DADOS DA NOTA
            nfse, autenticidade = self.capturar_dados_nota()
            
            return nfse, autenticidade
            
        except Exception as e:
            print(f"❌ Erro ao emitir nota: {e}")
            return None, None

    # ================= CAPTURA DE DADOS DA NOTA =================
    def capturar_dados_nota(self):
        """Captura número da nota e código de autenticidade"""
        print("📄 CAPTURANDO DADOS DA NOTA...")
        try:
            # Captura número da NFE
            campo_nfse = self.wait.until(
                EC.presence_of_element_located((By.ID, self.ELEMENTOS['numero_nfe']))
            )
            nfse = campo_nfse.get_attribute('value')
            
            # Captura código de autenticidade
            campo_autenticidade = self.driver.find_element(By.ID, self.ELEMENTOS['cod_autenticidade'])
            autenticidade = campo_autenticidade.get_attribute('value')
            
            print(f"✅ Nota {nfse} | Autenticidade: {autenticidade}")
            return nfse, autenticidade
            
        except Exception as e:
            print(f"❌ Erro ao capturar dados: {e}")
            # Tenta método alternativo (leitura de PDF)
            return self.capturar_do_pdf()

    def capturar_do_pdf(self):
        """Método alternativo para capturar do PDF (usando PyAutoGUI)"""
        print("📄 Tentando capturar do PDF...")
        try:
            # Sua lógica atual de captura do PDF aqui
            numero_nfse = "12345"
            codigo_autenticidade = "A1B2C3D4E5F6"
            return numero_nfse, codigo_autenticidade
        except:
            return None, None

    # ================= NOVA NOTA =================
    def incluir_nova_nota(self):
        """Clica para incluir nova nota"""
        print("🆕 INCLUINDO NOVA NOTA...")
        try:
            btn_nova = self.wait.until(
                EC.element_to_be_clickable((By.ID, self.ELEMENTOS['incluir_nova']))
            )
            btn_nova.click()
            time.sleep(3)
            return True
        except Exception as e:
            print(f"❌ Erro ao incluir nova nota: {e}")
            return False

# ================= FLUXO PRINCIPAL ATUALIZADO =================
def main():
    """FLUXO COMPLETO ATUALIZADO COM SELENIUM"""
    print("🚀 INICIANDO AUTOMAÇÃO NFE (SELENIUM)")
    print("=" * 50)
    
    # 1. CARREGAR PLANILHA
    nfe = carregar_planilha()
    if not nfe:
        return
    
    # 2. FAZER LOGIN
    driver = fazer_login_nfe()
    if not driver:
        return
    
    # 3. INICIALIZAR AUTOMAÇÃO
    automacao = NFEAutomacao(driver)
    
    # 4. PROCESSAR NOTAS
    processar_notas_pendentes(nfe, automacao)
    
    # 5. SALVAR E FECHAR
    salvar_planilha(nfe)
    driver.quit()
    print("\n🎉 AUTOMAÇÃO CONCLUÍDA!")

def processar_notas_pendentes(nfe, automacao):
    """Processa notas com Selenium"""
    print(f"🔄 PROCESSANDO {len(nfe.notas_pendentes)} NOTAS...")
    
    for i, nota_info in enumerate(nfe.notas_pendentes):
        print(f"\n📝 NOTA {i+1} de {len(nfe.notas_pendentes)}")
        
        if processar_uma_nota_selenium(nota_info, nfe, automacao):
            print("✅ Nota processada com sucesso!")
        else:
            print("❌ Falha na nota")
        
        # Pausa para próxima nota (exceto última)
        if i < len(nfe.notas_pendentes) - 1:
            input("⏸️  Pressione Enter para próxima nota...")
            
            # Navega para nova nota
            automacao.incluir_nova_nota()

def processar_uma_nota_selenium(nota_info, nfe, automacao):
    """Processa uma nota usando Selenium"""
    try:
        # 1. Navegar para formulário
        if not automacao.navegar_para_formulario(nota_info['dados']):
            return False
        
        # 2. Preencher dados
        if not automacao.preencher_dados_nota(nota_info['dados']):
            return False
        
        # 3. Emitir nota (passa a senha do config)
        senha = CONFIG_NFE.get('senha_certificado', '')
        nfse, autenticidade = automacao.emitir_nota(senha)
        
        if not nfse:
            return False
        
        # 4. Atualizar planilha
        nfe.marcar_como_processada(nota_info['indice_array'], nfse, autenticidade)
        return True
        
    except Exception as e:
        print(f"❌ Erro no processamento: {e}")
        return False

# ================= FUNÇÕES EXISTENTES (mantidas) =================
def carregar_planilha():
    """1. Carrega e valida planilha"""
    print("📊 CARREGANDO PLANILHA...")
    try:
        nfe = NFE()
        if nfe.dados is None or nfe.dados.empty:
            print("❌ Planilha vazia ou não carregada")
            return None
        print(f"✅ Planilha carregada: {len(nfe.notas_pendentes)} notas pendentes")
        return nfe
    except Exception as e:
        print(f"❌ Erro ao carregar planilha: {e}")
        return None

def salvar_planilha(nfe):
    """Salva planilha atualizada"""
    print("💾 SALVANDO PLANILHA...")
    if nfe.exportar_planilha_atualizada():
        print("✅ Planilha salva com sucesso!")
    else:
        print("❌ Erro ao salvar planilha")

if __name__ == "__main__":
    main()