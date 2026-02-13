from ..core.base_planilha import BasePlanilhaHandler

class ScantronPlanilhaHandler(BasePlanilhaHandler):
    """Handler para planilhas Scantron - baseado no código real"""
    
    def __init__(self):
        super().__init__("SCANTRON")
    
    def validar_estrutura(self):
        if self.df is None:
            return False, "Planilha não carregada"
        
        colunas_esperadas = ['Candidato', 'CPF', 'Valor', 'Data', 'Resultado']
        colunas_encontradas = [col for col in colunas_esperadas if col in self.df.columns]
        
        if len(colunas_encontradas) >= 3:
            return True, f"Estrutura Scantron válida - Colunas: {colunas_encontradas}"
        return False, f"Estrutura Scantron inválida - Colunas: {list(self.df.columns)}"
    
    def processar_linha(self, linha):
        return {
            'nome': linha.get('Candidato', ''),
            'cpf': linha.get('CPF', ''),
            'valor': linha.get('Valor', 0),
            'data': linha.get('Data', ''),
            'resultado': linha.get('Resultado', '')
        }
    
    def calcular_valor_total(self):
        if self.df is not None and 'Valor' in self.df.columns:
            return self.df['Valor'].sum()
        return 0
    
    def get_quantidade_candidatos(self):
        return len(self.df) if self.df is not None else 0