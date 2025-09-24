# modules/nfe/nfe_selecao.py
from .nfe_config import CONFIG_NFE

# Variável global para armazenar o tipo selecionado
_TIPO_PLANILHA = None

# 👇 MAPEAMENTO CORRETO DAS COLUNAS DE DATA
COLUNAS_DATA = {
    '103': '103',  # Planilha 103
    '43': 'Data Movto/\nCompetência'  # Planilha 43 (COM a quebra de linha)
}

def selecionar_tipo_planilha():
    """Seleciona o tipo de planilha UMA VEZ para toda a sessão"""
    global _TIPO_PLANILHA
    
    if _TIPO_PLANILHA:  # Já foi selecionado antes
        print(f"✅ Usando planilha {_TIPO_PLANILHA} (já selecionada)")
        return _TIPO_PLANILHA
    
    print("🎯 SELECIONANDO PLANILHA")
    print("=" * 50)
    print("1 - Planilha 103")
    print("2 - Planilha 43")
    
    while True:
        opcao = input("Digite o número da opção: ").strip()
        
        if opcao == "1":
            _TIPO_PLANILHA = '103'
        elif opcao == "2":
            _TIPO_PLANILHA = '43'
        else:
            print("❌ Opção inválida. Digite 1 ou 2.")
            continue
            
        caminho = CONFIG_NFE[f'caminho_planilha_{_TIPO_PLANILHA}']
        print(f"✅ Planilha {_TIPO_PLANILHA} selecionada")
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