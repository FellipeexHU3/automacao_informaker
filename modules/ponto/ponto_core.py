import pyautogui
import time
from datetime import datetime
import logging
from typing import Dict, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PontoAutomacao:
    def __init__(self, coordenadas: Dict):
        self.coordenadas = coordenadas
        self.ultimo_registro = None
        pyautogui.FAILSAFE = True
        logger.info("Sistema de ponto inicializado")
    
    def navegar_para_ponto(self):
        """Navega até o formulário de ponto"""
        try:
            logger.info("Navegando para formulário de ponto...")
            time.sleep(2)
            
            # Primeiro clique - Recepção
            pyautogui.click(self.coordenadas['menu_recepcao'])
            time.sleep(1.5)
            
            # Segundo clique - Horários
            pyautogui.click(self.coordenadas['menu_horarios'])
            time.sleep(3)
            
            logger.info("Navegação concluída com sucesso")
            return True
            
        except Exception as e:
            logger.error(f"Erro na navegação: {e}")
            return False
    
    def bater_ponto(self, tipo_ponto: str) -> bool:
        """
        Bate ponto de acordo com o tipo especificado
        Types: 'entrada', 'almoco', 'volta', 'saida'
        """
        try:
            if not self.navegar_para_ponto():
                return False
            
            logger.info(f"Registrando ponto: {tipo_ponto}")
            
            # Mapeamento de tipos para coordenadas
            mapeamento_botoes = {
                'entrada': self.coordenadas['botao_entrada'],
                'almoco': self.coordenadas['botao_almoco'],
                'volta': self.coordenadas['botao_volta'],
                'saida': self.coordenadas['botao_saida']
            }
            
            if tipo_ponto not in mapeamento_botoes:
                logger.error(f"Tipo de ponto inválido: {tipo_ponto}")
                return False
            
            # Clica no botão correspondente
            pyautogui.click(mapeamento_botoes[tipo_ponto])
            time.sleep(0.5)
            
            # Confirma o registro
            pyautogui.click(self.coordenadas['botao_confirmar'])
            time.sleep(0.5)
            
            self.ultimo_registro = {
                'tipo': tipo_ponto,
                'data_hora': datetime.now(),
                'status': 'sucesso'
            }
            
            logger.info(f"Ponto {tipo_ponto} registrado com sucesso!")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao bater ponto: {e}")
            self.ultimo_registro = {
                'tipo': tipo_ponto,
                'data_hora': datetime.now(),
                'status': 'erro',
                'erro': str(e)
            }
            return False
    
    def obter_ultimo_registro(self) -> Optional[Dict]:
        """Retorna informações do último registro"""
        return self.ultimo_registro
    
    def testar_coordenadas(self):
        """Testa todas as coordenadas configuradas"""
        logger.info("Testando coordenadas...")
        
        for nome, coord in self.coordenadas.items():
            try:
                logger.info(f"Testando {nome}: {coord}")
                pyautogui.moveTo(coord)
                time.sleep(0.5)
            except Exception as e:
                logger.error(f"Erro ao testar {nome}: {e}")
        
        logger.info("Teste de coordenadas concluído")