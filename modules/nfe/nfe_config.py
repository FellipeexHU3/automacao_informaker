# modules/nfe/nfe_config.py
from typing import Dict, List
import os
from dotenv import load_dotenv

load_dotenv()

CONFIG_NFE = {
    # CONFIGURAÇÕES GERAIS DO SISTEMA
    'url_nfe': os.getenv('URL_NFE'),
    'usuario': os.getenv('NFE_USUARIO'),
    'senha': os.getenv('NFE_SENHA'),
    'ir': os.getenv('NFE_INSCRICAO_MUNICIPAL'),
    
    # 👇 CAMINHOS DAS PLANILHAS
    'caminho_planilha_103': os.getenv('NFE_CAMINHO_PLANILHA_103'),
    'caminho_planilha_43': os.getenv('NFE_CAMINHO_PLANILHA_43'),
    'caminho_planilha_campinas_1': os.getenv('NFE_CAMINHO_PLANILHA_CAMPINAS_1'),
    'caminho_planilha_campinas_2': os.getenv('NFE_CAMINHO_PLANILHA_CAMPINAS_2'),
    # 👇 CONFIGURAÇÃO ESPECÍFICA DA PLANILHA 103 (CUIABÁ)
    'planilha_103': {
        'colunas': [
            'Data Movto/Competência',           # Data (DD/MM/AA)
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
        'campos_obrigatorios': ['Data Movto/Competência', 'RPS', 'CPF', 'Valor', 'Nome'],
        'colunas_processamento': ['NFSe', 'Autenticidade']
    },
    
    # 👇 CONFIGURAÇÃO ESPECÍFICA DA PLANILHA 43 (CUIABÁ)
    'planilha_43': {
        'colunas': [
            'Data Movto/Competência',  # Data
            'RPS',
            'CPF',
            'E-mail',
            'Dados NFSe',
            'Valor',
            'Aliq',
            'NFSe',
            'Autenticidade',
            'Unidade',
            'Nome',
            'CEP',
            'Endereço'
        ],
        'campos_obrigatorios': ['Data Movto/Competência', 'RPS', 'CPF', 'Valor', 'Nome'],
        'colunas_processamento': ['NFSe', 'Autenticidade']
    },
    
    # 👇 CONFIGURAÇÃO ESPECÍFICA DA PLANILHA CAMPINAS
    'planilha_campinas': {
        'colunas': [
            'Data Movimento', 'Nº RPS', 'Nº NF', 'Código', 
            'Tipo de Pessoa', 'CPF', 'Nome', 'NFLR_EMAIL_CLIENTE',
            'CEP', 'Descrição do Serviço', 'Valor', 'Endereço',
            'Bairro', 'Cidade', 'Estado', 'Código Atividade'
        ],
        'campos_obrigatorios': ['Data Movimento', 'Nº RPS', 'CPF', 'Valor', 'Nome'],
        'colunas_processamento': ['Nº NF', 'Código']
    }
}

# 👇 MAPEAMENTOS DE CAMPOS PARA CADA PLANILHA
MAPEAMENTO_CAMPOS_103 = {
    'Data Movto/Competência': 'data_emissao',
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

MAPEAMENTO_CAMPOS_43 = {
    'Data Movto/Competência': 'data_emissao',
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

MAPEAMENTO_CAMPOS_CAMPINAS = {
    'Data Movimento': 'data_emissao',
    'Nº RPS': 'numero_rps',
    'Nº NF': 'nfse',
    'Código': 'autenticidade',
    'Tipo de Pessoa': 'tipo_pessoa',
    'CPF': 'cpf_cliente',
    'Nome': 'nome_cliente',
    'NFLR_EMAIL_CLIENTE': 'email_cliente',
    'CEP': 'cep',
    'Descrição do Serviço': 'descricao_servico',
    'Valor': 'valor_servico',
    'Endereço': 'endereco',
    'Bairro': 'bairro',
    'Cidade': 'cidade',
    'Estado': 'estado',
    'Código Atividade': 'codigo_atividade'
}

# 👇 FUNÇÃO AUXILIAR PARA OBTER CONFIGURAÇÃO
def get_config_planilha(tipo_planilha):
    """Retorna configuração - campinas_1 e campinas_2 usam a mesma"""
    if tipo_planilha and tipo_planilha.startswith('campinas'):
        # campinas_1 e campinas_2 usam a MESMA configuração
        config_geral = CONFIG_NFE.get('planilha_campinas', {})
        mapeamento = MAPEAMENTO_CAMPOS_CAMPINAS
    elif tipo_planilha == '103':
        config_geral = CONFIG_NFE['planilha_103']
        mapeamento = MAPEAMENTO_CAMPOS_103
    elif tipo_planilha == '43':
        config_geral = CONFIG_NFE['planilha_43']
        mapeamento = MAPEAMENTO_CAMPOS_43
    else:
        config_geral = {}
        mapeamento = {}
    
    return {
        'colunas': config_geral.get('colunas', []),
        'campos_obrigatorios': config_geral.get('campos_obrigatorios', []),
        'colunas_processamento': config_geral.get('colunas_processamento', []),
        'mapeamento_campos': mapeamento
    }