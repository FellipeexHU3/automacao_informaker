# core/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    def __init__(self):
        # Suas variáveis de planilha

        self.CAMINHO_PLANILHA_PSI = os.getenv('CAMINHO_PLANILHA_PSI')
        self.COLUNA_VALOR_PSI = os.getenv('COLUNA_VALOR_PSI')
        self.NOME_ABA_PSI = os.getenv('NOME_ABA_PSI')

        self.CAMINHO_PLANILHA_VUE = os.getenv('CAMINHO_PLANILHA_VUE')
        self.COLUNA_VALOR_VUE = os.getenv('COLUNA_VALOR_VUE')
        self.NOME_ABA_VUE = os.getenv('NOME_ABA_VUE')

        self.CAMINHO_PLANILHA_KRYTERION = os.getenv('CAMINHO_PLANILHA_KRYTERION')
        self.COLUNA_VALOR_KRYTERION = os.getenv('COLUNA_VALOR_KRYTERION')
        self.NOME_ABA_KRYTERION = os.getenv('NOME_ABA_KRYTERION')

        self.URL_NFE=os.getenv('URL_NFE')
        self.NFE_USUARIO=os.getenv('NFE_USUARIO')
        self.NFE_SENHA=os.getenv('NFE_SENHA')
        self.NFE_INSCRICAO_MUNICIPAL=os.getenv('NFE_INSCRICAO_MUNICIPAL')
        self.NFE_CAMINHO_PLANILHA=os.getenv('NFE_CAMINHO_PLANILHA')

    def obter_caminho_planilha(self, tipo_planilha):
        if tipo_planilha == "VUE":
            return self.CAMINHO_PLANILHA_VUE
        elif tipo_planilha == "KRYTERION":
            return self.CAMINHO_PLANILHA_KRYTERION
        elif tipo_planilha == "PSI":
            return self.CAMINHO_PLANILHA_PSI
        return None

    def verificar_variaveis_env():
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

        
config = Config()

