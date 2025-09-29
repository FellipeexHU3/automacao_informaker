from ..core.base_planilha import BasePlanilhaHandler

class KryterionPlanilhaHandler(BasePlanilhaHandler):
    """Handler para planilhas Kryterion - baseado no código real"""
    
    def __init__(self):
        super().__init__("KRYTERION")
    
    def validar_estrutura(self):
        if self.df is None:
            return False, "Planilha não carregada"
        
        # Colunas Kryterion do seu código
        colunas_esperadas = ['Candidato', 'CPF/CNPJ', 'Valor', 'Data', 'Situação']
        colunas_encontradas = [col for col in colunas_esperadas if col in self.df.columns]
        
        if len(colunas_encontradas) >= 3:
            return True, f"Estrutura Kryterion válida - Colunas: {colunas_encontradas}"
        return False, f"Estrutura Kryterion inválida - Colunas: {list(self.df.columns)}"
    
    def processar_linha(self, linha):
        return {
            'nome': linha.get('Candidato', ''),
            'cpf': linha.get('CPF/CNPJ', ''),
            'valor': linha.get('Valor', 0),
            'data': linha.get('Data', ''),
            'situacao': linha.get('Situação', '')
        }
    
    def calcular_valor_total(self):
        if self.df is not None and 'Valor' in self.df.columns:
            return self.df['Valor'].sum()
        return 0
    
    def get_quantidade_candidatos(self):
        return len(self.df) if self.df is not None else 0
    
    def processar_planilha_kryterion(caminho_planilha):
    """Função compatível com o factory"""
    try:
        excel_file = pd.ExcelFile(caminho_planilha)
        coluna_valor = getattr(config, "COLUNA_VALOR_KRYTERION", None)
        
        abas_alvo = ["Mês 1", "Mês 2", "Mês 3"]
        total_geral = 0
        valor_total_geral = 0.0
        abas_processadas = []
        valores_por_aba = {}
        
        for aba in abas_alvo:
            if aba in excel_file.sheet_names:
                df_aba = pd.read_excel(caminho_planilha, sheet_name=aba, header=1)
                
                if coluna_valor and coluna_valor in df_aba.columns:
                    valores_validos = df_aba[coluna_valor].notna().sum()
                    valor_aba = df_aba[coluna_valor].sum()
                    
                    total_geral += valores_validos
                    valor_total_geral += valor_aba
                    abas_processadas.append(aba)
                    
                    valores_por_aba[aba] = {
                        "quantidade": int(valores_validos),
                        "valor_total": float(valor_aba)
                    }
        
        if not abas_processadas:
            return None
            
        return {
            "tipo": "KRYTERION",
            "quantidade": int(total_geral),
            "valor_total": float(valor_total_geral),
            "abas_processadas": abas_processadas,
            "valores_por_aba": valores_por_aba,
            "moeda": "US$"
        }
        
    except Exception as e:
        print(f"❌ Erro no handler KRYTERION: {e}")
        return None