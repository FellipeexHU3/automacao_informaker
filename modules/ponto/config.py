from typing import Dict

# Configurações de coordenadas (ajuste conforme sua tela)
COORDENADAS_PADRAO: Dict = {
    'menu_recepcao': (22, 362),
    'menu_horarios': (23, 200),
    'botao_entrada': (420, 375),
    'botao_almoco': (475, 375),
    'botao_volta': (530, 375),
    'botao_saida': (600, 375),
    'botao_confirmar': (1080, 375)
}

# Mapeamento de tipos de ponto
TIPOS_PONTO = {
    '1': 'entrada',
    '2': 'almoco',
    '3': 'volta',
    '4': 'saida'
}

NOMES_PONTO = {
    'entrada': 'Entrada',
    'almoco': 'Almoço',
    'volta': 'Volta do Almoço',
    'saida': 'Saída'
}