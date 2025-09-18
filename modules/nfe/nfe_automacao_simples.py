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
    'inscricao_municipal': (215, 315),
    'menu_emitir_nfe': (50, 290),
    'data_competencia': (1222, 375),
    'mostrar_rps': (280, 470),
    'numero_rps': (222, 520),
    'data_emissao': (560, 520), 
    'modelo_rps': (1000, 520),
    'modelo_rps2': (1000, 545),
    'campo_cpf': (333, 615),
    'campo_nome': (333, 640),
    'campo_valor': (333, 665),
    'campo_email': (740, 700),
    'campo_descricao': (300, 350),
    'campo_lc': (500, 400), 
    'campo_lc2': (500, 425),
    'campo_atv_municipio': (900, 400),
    'campo_atv_municipio2': (900, 425),
    'botao_emitir': (500, 500),
    'botao_confirmar': (680, 415),
    'numero_nfe': (1010, 383),
    'cod_autenticidade': (888, 500),
    'incluir_nova': (690, 690),
    'fora_quadrante': (1155, 411)
}

# ================= FUNÇÕES ESPECÍFICAS CAMPO A CAMPO =================
def navegar_para_formulario():
    """Navega até o formulário de emissão - PASSO A PASSO"""
    print("🗺️ NAVEGANDO PARA FORMULÁRIO...")
    try:
        # 1. Clica na inscrição municipal
        pyautogui.click(COORDENADAS['inscricao_municipal'])
        time.sleep(1)
        
        # 2. Preenche inscrição municipal (pega da config)
        inscricao = str(CONFIG_NFE.get('inscricao_municipal', ''))
        pyautogui.write(inscricao)
        time.sleep(0.5)
        
        # 3. Enter para confirmar
        pyautogui.press('enter')
        time.sleep(10)
        
        # 4. Clica no menu emitir NFE
        pyautogui.click(COORDENADAS['menu_emitir_nfe'])
        time.sleep(7)
        
        print("✅ Navegação concluída!")
        return True
        
    except Exception as e:
        print(f"❌ Erro na navegação: {e}")
        return False

def preencher_campos_nota(dados_nota):
    """Preenche CADA CAMPO individualmente com os dados da nota"""
    print("📝 PREENCHENDO CAMPOS DA NOTA...")
    try:
        # 👇 AGORA VOCÊ CONTROLA CADA CAMPO INDIVIDUALMENTE!
        
        # 1. Data de competência (campo 103 da planilha)
        pyautogui.click(COORDENADAS['data_competencia'])
        time.sleep(0.5)
        data_competencia = str(dados_nota.get('Campo103', ''))  # 👈 SEU CAMPO 103
        pyautogui.write(data_competencia)
        time.sleep(0.5)
        pyautogui.press('tab')
        time.sleep(0.3)
        
        # 2. Mostrar RPS
        pyautogui.click(COORDENADAS['mostrar_rps'])
        time.sleep(1)
        
        # 3. Número RPS (se tiver na planilha)
        pyautogui.click(COORDENADAS['numero_rps'])
        time.sleep(0.5)
        numero_rps = str(dados_nota.get('NumeroRPS', ''))
        pyautogui.write(numero_rps)
        time.sleep(0.5)
        pyautogui.press('tab')
        time.sleep(0.3)
        
        # 4. Data emissão (campo específico da planilha)
        pyautogui.click(COORDENADAS['data_emissao'])
        time.sleep(0.5)
        data_emissao = str(dados_nota.get('DataEmissao', ''))
        pyautogui.write(data_emissao)
        time.sleep(0.5)
        pyautogui.press('tab')
        time.sleep(0.3)
        
        # 5. CPF do cliente
        pyautogui.click(COORDENADAS['campo_cpf'])
        time.sleep(0.5)
        cpf = str(dados_nota.get('CPF', ''))
        pyautogui.write(cpf)
        time.sleep(0.5)
        pyautogui.press('tab')
        time.sleep(0.3)
        
        # 6. Nome do cliente
        pyautogui.click(COORDENADAS['campo_nome'])
        time.sleep(0.5)
        nome = str(dados_nota.get('Nome', ''))
        pyautogui.write(nome)
        time.sleep(0.5)
        pyautogui.press('tab')
        time.sleep(0.3)
        
        # 7. Valor da nota
        pyautogui.click(COORDENADAS['campo_valor'])
        time.sleep(0.5)
        valor = str(dados_nota.get('Valor', ''))
        pyautogui.write(valor)
        time.sleep(0.5)
        pyautogui.press('tab')
        time.sleep(0.3)
        
        # 8. Email (se necessário)
        pyautogui.click(COORDENADAS['campo_email'])
        time.sleep(0.5)
        email = str(dados_nota.get('Email', ''))
        pyautogui.write(email)
        time.sleep(0.5)
        pyautogui.press('tab')
        time.sleep(0.3)
        
        # 9. Descrição do serviço
        pyautogui.click(COORDENADAS['campo_descricao'])
        time.sleep(0.5)
        descricao = str(dados_nota.get('Descricao', ''))
        pyautogui.write(descricao)
        time.sleep(0.5)
        pyautogui.press('tab')
        time.sleep(0.3)
        
        print("✅ Todos os campos preenchidos!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao preencher campos: {e}")
        return False

def selecionar_opcoes_fixas():
    """Seleciona opções que são fixas (não variam por nota)"""
    print("🎯 SELECIONANDO OPÇÕES FIXAS...")
    try:
        # 1. Modelo RPS (opção fixa)
        pyautogui.click(COORDENADAS['modelo_rps'])
        time.sleep(1)
        pyautogui.press('down')  # Seleciona opção
        time.sleep(0.5)
        pyautogui.press('enter')
        time.sleep(1)
        
        # 2. Atividade municipal (opção fixa)
        pyautogui.click(COORDENADAS['campo_atv_municipio'])
        time.sleep(1)
        pyautogui.press('down')  # Seleciona opção
        time.sleep(0.5)
        pyautogui.press('enter')
        time.sleep(1)
        
        print("✅ Opções fixas selecionadas!")
        return True
        
    except Exception as e:
        print(f"❌ Erro nas opções fixas: {e}")
        return False

# ================= FLUXO PRINCIPAL =================
def processar_uma_nota(nota_info, nfe):
    """Processa UMA nota individual - CONTROLE TOTAL"""
    print(f"\n📝 PROCESSANDO NOTA {nota_info['indice_array'] + 1}")
    
    # 1. Navegar até formulário
    if not navegar_para_formulario():
        return False
    time.sleep(3)
    
    # 2. Preencher campos da NOTA (dados variáveis)
    if not preencher_campos_nota(nota_info['dados']):
        return False
    time.sleep(2)
    
    # 3. Selecionar opções FIXAS
    if not selecionar_opcoes_fixas():
        return False
    time.sleep(2)
    
    # 4. Gerar nota
    nfse, autenticidade = gerar_nota()
    if not nfse:
        return False
    
    # 5. Atualizar planilha
    nfe.marcar_como_processada(nota_info['indice_array'], nfse, autenticidade)
    print(f"✅ NFSe: {nfse} | Autenticidade: {autenticidade}")
    
    # 6. Preparar para próxima nota
    pyautogui.click(COORDENADAS['incluir_nova'])
    time.sleep(3)
    
    return True

def main():
    """FLUXO COMPLETO DA AUTOMAÇÃO NFE"""
    print("🚀 INICIANDO AUTOMAÇÃO NFE")
    print("=" * 50)
    
    # 1. Carregar planilha
    nfe = carregar_planilha()
    if not nfe:
        return
    
    # 2. Fazer login
    driver = fazer_login_nfe()
    if not driver:
        return
    
    print("✅ Login realizado! Iniciando automação em 5 segundos...")
    time.sleep(5)
    
    # 3. Processar notas
    processar_notas_pendentes(nfe)
    
    # 4. Salvar e finalizar
    salvar_planilha(nfe)
    driver.quit()

# ================= EXECUÇÃO =================
if __name__ == "__main__":
    main()
    print("\n🎉 AUTOMAÇÃO CONCLUÍDA!")