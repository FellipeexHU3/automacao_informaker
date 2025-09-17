from typing import List, Dict  # 👈 ADICIONAR ESTA LINHA

def __init__(self, caminho_planilha: str = None, dados: List[Dict] = None):
    """
    Inicializa o objeto NFE com dados de planilha ou array manual
    
    Args:
        caminho_planilha: Caminho para arquivo Excel/CSV
        dados: Array de dicionários com dados manuais
    """
    self.notas = []
    self.notas_pendentes = []
    self.notas_processadas = []
    self.dados = None
    
    # Usar caminho do .env se não especificado
    if caminho_planilha is None and CONFIG_NFE['caminho_planilha']:
        caminho_planilha = CONFIG_NFE['caminho_planilha']
    
    if caminho_planilha:
        self.carregar_de_planilha(caminho_planilha)  # 👈 Aqui chama _identificar_notas_pendentes()
    elif dados:
        self.carregar_de_array(dados)  # 👈 Aqui chama _identificar_notas_pendentes()
    else:
        logger.warning("NFE inicializado sem dados")
        # 👇 MESMO SEM DADOS, DEVE INICIALIZAR AS LISTAS VAZIAS
        self.notas_pendentes = []
        self.notas_processadas = []