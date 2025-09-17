# core/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    def __init__(self):
        # Suas variáveis de planilha
        self.CAMINHO_PLANILHA_VUE = os.getenv('CAMINHO_PLANILHA_VUE')
        self.COLUNA_VALOR_VUE = os.getenv('COLUNA_VALOR_VUE')
        self.NOME_ABA_VUE = os.getenv('NOME_ABA_VUE')
        # ... outras variáveis ...
        
config = Config()

def verificar_variaveis_env():
    """Verifica se todas variáveis do .env estão configuradas"""
    print("\n🔍 VERIFICANDO VARIÁVEIS DO .ENV...")
    print("=" * 50)

    variaveis = [
        'CAMINHO_PLANILHA_VUE', 'COLUNA_VALOR_VUE', 'NOME_ABA_VUE',
        'CAMINHO_PLANILHA_KRYTERION', 'COLUNA_VALOR_KRYTERION', 'NOME_ABA_KRYTERION', 
        'CAMINHO_PLANILHA_PSI', 'COLUNA_VALOR_PSI', 'NOME_ABA_PSI'
    ]

    for var in variaveis:
        valor = os.getenv(var)
        status = "✅" if valor else "❌"
        print(f"{status} {var}: {valor}")