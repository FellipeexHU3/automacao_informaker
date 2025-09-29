# modules/planilhas/handlers/vue_handler.py
from ..core.base_planilha import BasePlanilhaHandler
import pandas as pd
from core.config import config

class VuePlanilhaHandler(BasePlanilhaHandler):
    """Handler para planilhas VUE"""
    
    def __init__(self):
        super().__init__("VUE")
    
    def validar_estrutura(self):
        if self.df is None:
            return False, "Planilha não carregada"
        
        print("🔍 Colunas encontradas:", list(self.df.columns))
        
        colunas_esperadas = ['Cliente ', 'Valor']
        colunas_encontradas = [col for col in colunas_esperadas if col in self.df.columns]
        
        if len(colunas_encontradas) >= 1:
            return True, f"Estrutura VUE válida - Colunas: {colunas_encontradas}"
        return False, f"Estrutura VUE inválida - Colunas: {list(self.df.columns)}"
    
    def processar_linha(self, linha):
        return {
            'cliente': linha.get('Cliente ', ''),
            'valor': linha.get('Valor', 0)
        }

def processar_planilha_vue(caminho_planilha):
    """Função compatível com o factory - VERSÃO SIMPLIFICADA"""
    try:
        print(f"🔧 Handler VUE processando: {caminho_planilha}")
        
        # Lógica direta do sistema tradicional
        df = pd.read_excel(caminho_planilha, sheet_name=getattr(config, "NOME_ABA_VUE", 0), header=0)
        coluna_valor = getattr(config, "COLUNA_VALOR_VUE", None)
        
        valor_total = 0.0
        if coluna_valor and coluna_valor in df.columns:
            valor_total = df[coluna_valor].sum()
        
        # Lógica de clientes
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
        
        resultado = {
            "tipo": "VUE",
            "quantidade": int(len(df)),
            "valor_total": float(valor_total),
            "moeda": "US$",
            "relatorio_detalhado": relatorio_detalhado
        }
        
        print(f"✅ Handler VUE finalizado: {resultado['quantidade']} candidatos")
        return resultado
        
    except Exception as e:
        print(f"❌ Erro no handler VUE: {e}")
        return None