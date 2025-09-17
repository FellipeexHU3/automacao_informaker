import pyautogui
import time
import sys
import os
from datetime import datetime
from modules.nfe.nfe_planilha_teste import testar_planilha
from modules.nfe.nfe_core import NFE
from modules.nfe.nfe_config import CONFIG_NFE
from modules.login.modulo_login_nfe import fazer_login_nfe
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# ================= CONFIGURAÇÕES =================
COORDENADAS = {
    'inscricao_municipal': (200, 100),
    'menu_principal': (100, 100),
    'menu_nfse': (120, 150),
    'emitir_nfse': (150, 200),
    'campo_cpf': (300, 250),
    'campo_nome': (300, 280),
    'campo_valor': (300, 310),
    'botao_emitir': (500, 500),
    'botao_confirmar': (550, 550)
}

# ================= FUNÇÕES DE PREENCHIMENTO =================
def preencher_dados(dados):
    """Preenche dados no formulário da NFSe"""
    print("📝 PREENCHENDO DADOS...")
    try:
        # CPF
        pyautogui.click(COORDENADAS['campo_cpf'])
        pyautogui.write(str(dados.get('CPF', '')))
        time.sleep(0.5)
        
        # Nome
        pyautogui.click(COORDENADAS['campo_nome'])
        pyautogui.write(str(dados.get('Nome', '')))
        time.sleep(0.5)
        
        # Valor
        pyautogui.click(COORDENADAS['campo_valor'])
        pyautogui.write(str(dados.get('Valor', '')))
        time.sleep(0.5)
        
        print("✅ Dados preenchidos com sucesso!")
        return True
    except Exception as e:
        print(f"❌ Erro ao preencher dados: {e}")
        return False

def navegar_para_formulario_selenium(driver):
    """Navega e preenche a inscrição municipal no campo txtCae"""
    print("🗺️ NAVEGANDO E PREENCHENDO INSCRIÇÃO MUNICIPAL...")
    try:
        """ # 1. Primeiro navega até o formulário (seus cliques anteriores)
        pyautogui.click(COORDENADAS['inscricao_municipal'])
        time.sleep(1)
        pyautogui.write(str(dados.get('ir', '')))
         """
        # 2. 👇 AGORA USA SELENIUM PARA PREENCHER O CAMPO txtCae
        print("📝 PREENCHENDO INSCRIÇÃO MUNICIPAL...")
        
        # Espera o campo txtCae ficar disponível
        campo_cae = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "txtCae"))
        )
        
        # Limpa o campo (se tiver algo)
        campo_cae.clear()
        
        # Pega a inscrição municipal das variáveis globais
        from modules.nfe.nfe_config import CONFIG_NFE
        inscricao_municipal = CONFIG_NFE['inscricao_municipal']
        
        # Preenche o campo
        campo_cae.send_keys(inscricao_municipal)
        print(f"✅ Inscrição municipal '{inscricao_municipal}' preenchida!")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao preencher inscrição municipal: {e}")
        return False
def navegar_para_formulario():
    """Navega até o formulário de emissão"""
    print("🗺️ NAVEGANDO PARA FORMULÁRIO...")
    try:
        pyautogui.click(COORDENADAS['inscricao_municipal'])
        time.sleep(1)
        return True
    except Exception as e:
        print(f"❌ Erro ao navegar: {e}")
        return False

def gerar_nota():
    """Gera a nota e captura dados do PDF"""
    print("🚀 GERANDO NOTA...")
    try:
        pyautogui.click(COORDENADAS['botao_emitir'])
        time.sleep(3)
        pyautogui.click(COORDENADAS['botao_confirmar'])
        time.sleep(5)
        
        # 👇 VOCÊ VAI IMPLEMENTAR A CAPTURA REAL DO PDF AQUI!
        nfse, autenticidade = capturar_dados_do_pdf()
        
        return nfse, autenticidade
    except Exception as e:
        print(f"❌ Erro ao gerar nota: {e}")
        return None, None

def capturar_dados_do_pdf():
    """FUNÇÃO QUE VOCÊ VAI IMPLEMENTAR PARA CAPTURAR DO PDF"""
    print("📄 CAPTURANDO DADOS DO PDF...")
    
    # EXEMPLO - SUBSTITUA PELA CAPTURA REAL!
    numero_nfse = "12345"  # 👈 Isso virá do PDF
    codigo_autenticidade = "A1B2C3D4E5F6"  # 👈 Isso virá do PDF
    
    return numero_nfse, codigo_autenticidade

def carregar_planilha():
    """1. Carrega e valida planilha"""
    print("📊 CARREGANDO PLANILHA...")
    try:
        nfe = NFE()
        
        # 👇 VERIFICA SE OS DADOS FORAM CARREGADOS CORRETAMENTE
        if nfe.dados is None or nfe.dados.empty:
            print("❌ Planilha vazia ou não carregada")
            return None
            
        print(f"✅ Planilha carregada: {len(nfe.notas_pendentes)} notas pendentes")
        print(f"📋 Total de linhas: {len(nfe.dados)}")
        
        # 👇 AGORA ESTE ACESSO VAI FUNCIONAR
        if hasattr(nfe.dados, 'columns'):
            print(f"📋 Colunas: {list(nfe.dados.columns)}")
        
        return nfe
        
    except Exception as e:
        print(f"❌ Erro ao carregar planilha: {e}")
        return None

def salvar_planilha(nfe):
    """4. Salva planilha atualizada"""
    print("💾 SALVANDO PLANILHA...")
    if nfe.exportar_planilha_atualizada():
        print("✅ Planilha salva com sucesso!")
    else:
        print("❌ Erro ao salvar planilha")

def testar_login():
    """2. Testa login no sistema"""
    print("🔐 TESTANDO LOGIN...")
    driver = fazer_login_nfe()
    if driver:
        print("✅ Login testado com sucesso!")
        return True
    print("❌ Falha no login")
    return False

# ================= FLUXO PRINCIPAL =================
def main():
    """FLUXO COMPLETO DA AUTOMAÇÃO NFE"""
    print("🚀 INICIANDO AUTOMAÇÃO NFE")
    print("=" * 50)
    
    # 1. CARREGAR PLANILHA
    nfe = carregar_planilha()
    if not nfe:
        return
    
    # 2. FAZER LOGIN COM SELENIUM
    driver = fazer_login_nfe()
    if not driver:
        return
    
    # 3. 👇 AGORA USA A NOVA FUNÇÃO COM SELENIUM
    if not navegar_para_formulario_selenium(driver):
        print("❌ Falha na navegação - abortando")
        driver.quit()
        return
    
    # 4. 👇 DEPOIS USA PYAUTOGUI PARA PREENCHER (se quiser)
    processar_notas_pendentes(nfe)  # Esta ainda usa PyAutoGUI
    
    # 5. SALVAR E FECHAR
    salvar_planilha(nfe)
    driver.quit()


def processar_notas_pendentes(nfe):
    """3. Processa todas as notas pendentes com pausa manual"""
    print("🔄 PROCESSANDO NOTAS PENDENTES...")
    print("⏸️  O sistema pausará após cada nota - pressione Enter para continuar")
    
    for i, nota_info in enumerate(nfe.notas_pendentes[:]):
        print(f"\n📝 PROCESSANDO NOTA {i+1} de {len(nfe.notas_pendentes)}")
        print(f"📋 Linha da planilha: {nota_info['indice_planilha']}")
        
        if processar_uma_nota(nota_info, nfe):
            print("✅ Nota processada com sucesso!")
        else:
            print("❌ Falha na nota")
        
        # 👇 AGORA ESPERA ENTER PARA PRÓXIMA NOTA
        if i < len(nfe.notas_pendentes) - 1:  # Não pergunta na última
            input("⏸️  Pressione Enter para processar próxima nota...")
        else:
            print("🎉 Última nota processada!")

def processar_uma_nota(nota_info, nfe):
    """Processa UMA nota individual"""
    print(f"\n📝 PROCESSANDO NOTA {nota_info['indice_array'] + 1}")
    
    # A. NAVEGAR ATÉ FORMULÁRIO
    if not navegar_para_formulario():
        return False
    
    # B. PREENCHER DADOS
    if not preencher_dados(nota_info['dados']):
        return False
    
    # C. GERAR NOTA
    nfse, autenticidade = gerar_nota()
    if not nfse:
        return False
    
    # D. ATUALIZAR PLANILHA
    nfe.marcar_como_processada(nota_info['indice_array'], nfse, autenticidade)
    print(f"✅ NFSe: {nfse} | Autenticidade: {autenticidade}")
    
    return True


# ================= EXECUÇÃO =================
if __name__ == "__main__":
    main()
    print("\n🎉 AUTOMAÇÃO CONCLUÍDA!")