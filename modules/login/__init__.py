from modules.nfe.nfe_core import NFE
__all__ = ['NFE', 'main']

from .modulo_login_nfe import (
    fazer_login_nfe, 
    verificar_login_nfe, 
    fazer_logout_nfe,
    testar_coordenadas_nfe,
    get_credenciais_nfe
)

__all__ = [
    'fazer_login_nfe', 
    'verificar_login_nfe', 
    'fazer_logout_nfe',
    'testar_coordenadas_nfe',
    'get_credenciais_nfe'
]