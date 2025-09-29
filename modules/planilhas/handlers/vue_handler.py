import sys
import os

# Corrige path de importação
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from modules.planilhas.core.base_planilha import BasePlanilhaHandler
import pandas as pd

class VuePlanilhaHandler(BasePlanilhaHandler):
    """Handler para planilhas VUE"""
    
    def __init__(self):
        super().__init__("VUE")
    
    def validar_estrutura(self):
        if self.df is None:
            return False, "Planilha não carregada"
        
        print("🔍 Colunas encontradas:", list(self.df.columns))
        
        colunas_esperadas = ['Nome', 'CPF', 'Valor', 'Data', 'Status']
        colunas_encontradas = [col for col in colunas_esperadas if col in self.df.columns]
        
        if len(colunas_encontradas) >= 3:
            return True, f"Estrutura VUE válida - Colunas: {colunas_encontradas}"
        return False, f"Estrutura VUE inválida - Colunas: {list(self.df.columns)}"
    
    def processar_linha(self, linha):
        return {
            'nome': linha.get('Nome', ''),
            'cpf': linha.get('CPF', ''),
            'valor': linha.get('Valor', 0),
            'data': linha.get('Data', ''),
            'status': linha.get('Status', '')
        }
    def processar_planilha_vue(caminho_planilha):
    """Função compatível com o factory"""
    try:
        handler = VuePlanilhaHandler()
        handler.carregar_planilha(caminho_planilha)
        
        # Aqui você adapta a lógica do seu sistema tradicional VUE
        df = pd.read_excel(caminho_planilha, sheet_name=getattr(config, "NOME_ABA_VUE", 0), header=0)
        coluna_valor = getattr(config, "COLUNA_VALOR_VUE", None)
        
        valor_total = 0.0
        if coluna_valor and coluna_valor in df.columns:
            valor_total = df[coluna_valor].sum()
        
        # Lógica de clientes (do sistema tradicional)
        relatorio_detalhado = []
        if 'Cliente ' in df.columns:
            clientes_validos = df["Cliente "].dropna().astype(str)
            contagem_clientes = clientes_validos.value_counts()
            total_geral = len(clientes_validos)
            
            for cliente, quantidade in contagem_clientes.items():
                percentual = (quantidade / total_geral) * 100
                relatorio_detalhado.append({
                    'cliente': cliente,
                    'quantidade': quantidade,
                    'percentual': percentual
                })
        
        return {
            "tipo": "VUE",
            "quantidade": int(len(df)),
            "valor_total": float(valor_total),
            "moeda": "US$",
            "relatorio_detalhado": relatorio_detalhado
        }
        
    except Exception as e:
        print(f"❌ Erro no handler VUE: {e}")
        return None