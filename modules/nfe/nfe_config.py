# modulo_nfe/nfe_config.py (certifique-se que tem isso)
from typing import Dict, List
import os
from dotenv import load_dotenv

load_dotenv()

CONFIG_NFE = {
    'url_nfe': os.getenv('URL_NFE'),
    'usuario': os.getenv('NFE_USUARIO'),
    'senha': os.getenv('NFE_SENHA'),
    'ir': os.getenv('NFE_INSCRICAO_MUNICIPAL'),
    'caminho_planilha': os.getenv('NFE_CAMINHO_PLANILHA'),
    'colunas_planilha': [
        '103',           # Data (DD/MM/AA)
        'RPS',           # Número do RPS
        'CPF',           # CPF do cliente
        'E-mail',        # E-mail do cliente
        'Dados NFSe',    # Dados da NFSe
        'Valor',         # Valor do serviço
        'Aliq',          # Alíquota
        'NFSe',          # Número da NFSe (gerado pelo sistema)
        'Autenticidade', # Código de autenticidade
        'Unidade',       # Unidade
        'Nome',          # Nome do cliente
        'CEP',           # CEP
        'Endereço'       # Endereço completo
    ],
    
    # Campos obrigatórios para validação
    'campos_obrigatorios': ['103', 'RPS', 'CPF', 'Valor', 'Nome'],
    
    'colunas_processamento': ['NFSe', 'Autenticidade']
}

MAPEAMENTO_CAMPOS = {
    '103': 'data_emissao',
    'RPS': 'numero_rps',
    'CPF': 'cpf_cliente',
    'E-mail': 'email_cliente',
    'Dados NFSe': 'dados_nfse',
    'Valor': 'valor_servico',
    'Aliq': 'aliquota',
    'Unidade': 'unidade',
    'Nome': 'nome_cliente',
    'CEP': 'cep',
    'Endereço': 'endereco'
}