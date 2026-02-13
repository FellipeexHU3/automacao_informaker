# modules/planilhas/core/base_planilha.py
from abc import ABC, abstractmethod
import pandas as pd
import logging

class BasePlanilhaHandler(ABC):
    """Classe base para todos os handlers de planilha"""
    
    def __init__(self, nome_planilha):
        self.nome_planilha = nome_planilha
        self.df = None
        self.logger = logging.getLogger(f"planilha.{nome_planilha}")
    
    def carregar_planilha(self, caminho):
        """Carrega planilha - comum a todos"""
        try:
            self.df = pd.read_excel(caminho)
            self.logger.info(f"✅ Planilha carregada: {len(self.df)} linhas")
            return self.df
        except Exception as e:
            self.logger.error(f"❌ Erro ao carregar: {e}")
            raise
    
    @abstractmethod
    def validar_estrutura(self):
        """Valida estrutura específica da planilha"""
        pass
        
    @abstractmethod
    def processar_linha(self, linha):
        """Processa linha conforme tipo de planilha"""
        pass
    
    def get_info_basica(self):
        """Info básica comum a todas"""
        if self.df is not None:
            return {
                'linhas': len(self.df),
                'colunas': list(self.df.columns),
                'tipo': self.nome_planilha
            }
        return {}
    
    def calcular_valor_total(self):
        """Calcula valor total - implementação base"""
        if self.df is not None and 'Valor' in self.df.columns:
            return self.df['Valor'].sum()
        return 0
    
    def get_quantidade_candidatos(self):
        """Retorna quantidade de candidatos"""
        return len(self.df) if self.df is not None else 0