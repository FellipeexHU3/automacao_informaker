# modulo_nfe/nfe_automacao_simples.py
import pyautogui
import time
from datetime import datetime

# ================= CONFIGURAÇÕES DIRETO NO CÓDIGO =================
# COORDENADAS FICTÍCIAS - AJUSTE COM AS SUAS!
COORDENADAS = {
    'campo_usuario': (230, 280),
    'campo_senha': (230, 320),
    'botao_login': (230, 360),
    'menu_nfse': (100, 100),
    'emitir_nfse': (150, 150),
    'campo_data': (300, 250),
    'campo_cpf': (300, 280),
    'campo_nome': (300, 310),
    'campo_valor': (300, 340),
    'campo_email': (300, 370),
    'botao_emitir': (500, 500),
    'botao_confirmar': (550, 550)
}

TEMPOS = {
    'login': 2,
    'navegacao': 1,
    'preenchimento': 0.5,
    'processamento': 3
}

# ================= FUNÇÕES PURAS - SEM CLASSES =================

def fazer_login_nfe_pyautogui(usuario, senha):
    """Faz login no sistema NFE usando PyAutoGUI"""
    print("🔐 FAZENDO LOGIN...")
    
    try:
        # Campo usuário
        pyautogui.click(COORDENADAS['campo_usuario'])
        time.sleep(TEMPOS['preenchimento'])
        pyautogui.write(usuario)
        
        # Campo senha
        pyautogui.click(COORDENADAS['campo_senha'])
        time.sleep(TEMPOS['preenchimento'])
        pyautogui.write(senha)
        
        # Botão login
        pyautogui.click(COORDENADAS['botao_login'])
        time.sleep(TEMPOS['login'])
        
        print("✅ Login realizado!")
        return True
        
    except Exception as e:
        print(f"❌ Erro no login: {e}")
        return False

def navegar_para_emissao():
    """Navega até a tela de emissão de NFSe"""
    print("🗺️ NAVEGANDO PARA EMISSÃO...")
    
    try:
        pyautogui.click(COORDENADAS['menu_nfse'])
        time.sleep(TEMPOS['navegacao'])
        
        pyautogui.click(COORDENADAS['emitir_nfse'])
        time.sleep(TEMPOS['navegacao'])
        
        print("✅ Navegação concluída!")
        return True
        
    except Exception as e:
        print(f"❌ Erro na navegação: {e}")
        return False

def preencher_dados_nota(dados_nota):
    """Preenche os dados da nota fiscal"""
    print("📝 PREENCHENDO DADOS...")
    
    try:
        # Data (campo 103)
        if '103' in dados_nota:
            pyautogui.click(COORDENADAS['campo_data'])
            time.sleep(TEMPOS['preenchimento'])
            pyautogui.write(str(dados_nota['103']))
        
        # CPF
        if 'CPF' in dados_nota:
            pyautogui.click(COORDENADAS['campo_cpf'])
            time.sleep(TEMPOS['preenchimento'])
            pyautogui.write(str(dados_nota['CPF']))
        
        # Nome
        if 'Nome' in dados_nota:
            pyautogui.click(COORDENADAS['campo_nome'])
            time.sleep(TEMPOS['preenchimento'])
            pyautogui.write(str(dados_nota['Nome']))
        
        # Valor
        if 'Valor' in dados_nota:
            pyautogui.click(COORDENADAS['campo_valor'])
            time.sleep(TEMPOS['preenchimento'])
            pyautogui.write(str(dados_nota['Valor']))
        
        # Email
        if 'E-mail' in dados_nota:
            pyautogui.click(COORDENADAS['campo_email'])
            time.sleep(TEMPOS['preenchimento'])
            pyautogui.write(str(dados_nota['E-mail']))
        
        print("✅ Dados preenchidos!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao preencher: {e}")
        return False

def emitir_nota():
    """Emite a nota fiscal e retorna os dados"""
    print("🚀 EMITINDO NOTA...")
    
    try:
        pyautogui.click(COORDENADAS['botao_emitir'])
        time.sleep(TEMPOS['processamento'])
        
        pyautogui.click(COORDENADAS['botao_confirmar'])
        time.sleep(TEMPOS['processamento'])
        
        # Simula geração da NFSe (você vai adaptar para capturar do sistema)
        nfse = f"NFSE{datetime.now().strftime('%Y%m%d%H%M')}"
        autenticidade = f"AUT{datetime.now().strftime('%H%M%S')}"
        
        print(f"✅ Nota emitida! {nfse}")
        return nfse, autenticidade
        
    except Exception as e:
        print(f"❌ Erro ao emitir: {e}")
        return None, None

def processar_nota_simples(dados_nota, usuario, senha):
    """Processa uma nota completa - FUNÇÃO PRINCIPAL"""
    print(f"🔄 PROCESSANDO NOTA - {dados_nota.get('Nome', 'Cliente')}")
    print("=" * 50)
    
    # Login
    if not fazer_login_nfe_pyautogui(usuario, senha):
        return False, None, None
    
    # Navegação
    if not navegar_para_emissao():
        return False, None, None
    
    # Preenchimento
    if not preencher_dados_nota(dados_nota):
        return False, None, None
    
    # Emissão
    nfse, autenticidade = emitir_nota()
    
    if nfse and autenticidade:
        print("🎉 NOTA PROCESSADA COM SUCESSO!")
        return True, nfse, autenticidade
    
    return False, None, None

# ================= FUNÇÃO DE TESTE =================

def testar_coordenadas():
    """Testa todas as coordenadas configuradas"""
    print("🎯 TESTANDO COORDENADAS")
    print("=" * 50)
    
    for nome, coord in COORDENADAS.items():
        print(f"Testando {nome}: {coord}")
        pyautogui.moveTo(coord)
        time.sleep(0.5)
    
    print("✅ Teste de coordenadas concluído!")