from ..core.base_planilha import BasePlanilhaHandler

class PsiPlanilhaHandler(BasePlanilhaHandler):
    """Handler para planilhas PSI - baseado no código real"""
    
    def __init__(self):
        super().__init__("PSI")
    
    def validar_estrutura(self):
        if self.df is None:
            return False, "Planilha não carregada"
        
        colunas_esperadas = ['Nome Completo', 'Documento', 'Valor', 'Data Exame', 'Status']
        colunas_encontradas = [col for col in colunas_esperadas if col in self.df.columns]
        
        if len(colunas_encontradas) >= 3:
            return True, f"Estrutura PSI válida - Colunas: {colunas_encontradas}"
        return False, f"Estrutura PSI inválida - Colunas: {list(self.df.columns)}"
    
    def processar_linha(self, linha):
        return {
            'nome': linha.get('Nome Completo', ''),
            'cpf': linha.get('Documento', ''),
            'valor': linha.get('Valor', 0),
            'data': linha.get('Data Exame', ''),
            'status': linha.get('Status', '')
        }
    
    def calcular_valor_total(self):
        if self.df is not None and 'Valor' in self.df.columns:
            return self.df['Valor'].sum()
        return 0
    
    def get_quantidade_candidatos(self):
        return len(self.df) if self.df is not None else 0