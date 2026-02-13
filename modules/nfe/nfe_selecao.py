# modules/nfe/nfe_selecao.py
from .nfe_config import CONFIG_NFE

# Variável global para armazenar o tipo selecionado
_TIPO_PLANILHA = None

# 👇 MAPEAMENTO CORRETO DAS COLUNAS DE DATA
COLUNAS_DATA = {
    '103': 'Data Movto/\nCompetência',  # Planilha 103
    '43': 'Data Movto/\nCompetência'  # Planilha 43 (COM a quebra de linha)
}

def selecionar_tipo_planilha():
    global _TIPO_PLANILHA
    
    if _TIPO_PLANILHA:
        return _TIPO_PLANILHA
    
    print("🎯 SELECIONANDO PLANILHA")
    print("=" * 50)
    print("1 - Planilha 103 (Cuiabá)")
    print("2 - Planilha 43 (Cuiabá)") 
    print("3 - Planilha Campinas")
    print("=" * 50)
    
    while True:
        opcao = input("Digite o número da opção: ").strip()
        
        if opcao == "1":
            _TIPO_PLANILHA = '103'
            caminho = CONFIG_NFE['caminho_planilha_103']
            
        elif opcao == "2":
            _TIPO_PLANILHA = '43'
            caminho = CONFIG_NFE['caminho_planilha_43']
            
        elif opcao == "3":
            # 👇 SUBSELECÇÃO SIMPLES
            print("\n📅 SELECIONAR QUINZENA:")
            print("1 - Primeira Quinzena")
            print("2 - Segunda Quinzena")
            
            quinzena = input("Digite 1 ou 2: ").strip()
            if quinzena == "1":
                _TIPO_PLANILHA = 'campinas_1'
                caminho = CONFIG_NFE['caminho_planilha_campinas_1']
            elif quinzena == "2":
                _TIPO_PLANILHA = 'campinas_2' 
                caminho = CONFIG_NFE['caminho_planilha_campinas_2']
            else:
                print("❌ Opção inválida")
                continue
                
        else:
            print("❌ Opção inválida. Digite 1, 2 ou 3.")
            continue
        
        print(f"✅ {_TIPO_PLANILHA} selecionada")
        return _TIPO_PLANILHA
        
def get_coluna_data(tipo_planilha=None):
    """Retorna o nome correto da coluna de data"""
    if not tipo_planilha:
        tipo_planilha = get_tipo_planilha()
    return COLUNAS_DATA.get(tipo_planilha)

def get_caminho_planilha():
    """Retorna o caminho da planilha baseado no tipo selecionado"""
    if not _TIPO_PLANILHA:
        selecionar_tipo_planilha()
    return CONFIG_NFE[f'caminho_planilha_{_TIPO_PLANILHA}']

def get_tipo_planilha():
    """Retorna o tipo de planilha selecionado"""
    if not _TIPO_PLANILHA:
        selecionar_tipo_planilha()
    return _TIPO_PLANILHA

def reset_selecao():
    """Reseta a seleção (útil para testes)"""
    global _TIPO_PLANILHA
    _TIPO_PLANILHA = None

# modules/nfe/nfe_selecao.py - ATUALIZAR
from .nfe_config import CONFIG_NFE, get_config_planilha

# 👇 SIMPLIFICAR - AGORA USA A FUNÇÃO get_config_planilha
def get_config_planilha(tipo_planilha=None):
    """Retorna configuração específica para o tipo de planilha"""
    if not tipo_planilha:
        tipo_planilha = get_tipo_planilha()
    return get_config_planilha(tipo_planilha)