import pandas as pd
from typing import List, Dict, Optional
import logging
from datetime import datetime
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from modules.nfe.nfe_config import CONFIG_NFE, MAPEAMENTO_CAMPOS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NFE:
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
        
        # Usar caminho do .env se não especificado
        if caminho_planilha is None and CONFIG_NFE['caminho_planilha']:
            caminho_planilha = CONFIG_NFE['caminho_planilha']
        
        if caminho_planilha:
            self.carregar_de_planilha(caminho_planilha)
        elif dados:
            self.carregar_de_array(dados)
        else:
            logger.warning("NFE inicializado sem dados")
    
    def carregar_de_planilha(self, caminho_planilha: str):
        """Carrega dados de uma planilha Excel"""
        try:
            # Ler planilha mantendo o formato original das colunas
            df = pd.read_excel(caminho_planilha)
            self.dados = df  # 👈 ARMAZENA O DATAFRAME COMPLETO
            self.notas = df.to_dict('records')
            
            logger.info(f"Carregadas {len(self.notas)} notas da planilha: {caminho_planilha}")
            self._identificar_notas_pendentes()
            
        except Exception as e:
            logger.error(f"Erro ao carregar planilha {caminho_planilha}: {e}")
            raise
    
    def carregar_de_array(self, dados: List[Dict]):
        """Carrega dados de um array manual"""
        self.notas = dados
        self.dados = pd.DataFrame(dados)  # 👈 CONVERTE ARRAY PARA DATAFRAME
        logger.info(f"Carregadas {len(self.notas)} notas do array")
        self._identificar_notas_pendentes()
    
    def _identificar_notas_pendentes(self):
        """Identifica quais notas ainda não foram processadas"""
        self.notas_pendentes = []
        self.notas_processadas = []
        
        coluna_nfse, coluna_auth = CONFIG_NFE['colunas_processamento']
        
        for i, nota in enumerate(self.notas):
            # Verifica se NFSe e Autenticidade estão preenchidos
            nfse_preenchido = self._campo_preenchido(nota.get(coluna_nfse))
            autenticidade_preenchida = self._campo_preenchido(nota.get(coluna_auth))
            
            if nfse_preenchido and autenticidade_preenchida:
                self.notas_processadas.append({
                    'indice_planilha': i + 2,  # +2 porque Excel começa na linha 1 + header
                    'indice_array': i,
                    'dados': nota,
                    'status': 'processada'
                })
            else:
                self.notas_pendentes.append({
                    'indice_planilha': i + 2,
                    'indice_array': i,
                    'dados': nota,
                    'status': 'pendente'
                })
        
        logger.info(f"Encontradas {len(self.notas_pendentes)} notas pendentes")
        logger.info(f"Encontradas {len(self.notas_processadas)} notas processadas")
    
    def _campo_preenchido(self, valor) -> bool:
        if valor is None:
            return False
            
        if isinstance(valor, (int, float)):
            # 👇 Só considerar preenchido se for maior que 0
            return valor > 0
            
        if isinstance(valor, str):
            valor = valor.strip()
            # 👇 Ignorar valores inválidos, zeros, etc.
            invalid_values = ['', 'NaN', 'NULL', 'None', 'NaT', '0', '0.0', '0,0']
            return valor not in invalid_values and not valor.startswith('NFSe') and len(valor) > 3
            
        return False
    
    def obter_proxima_nota_pendente(self) -> Optional[Dict]:
        """Retorna a próxima nota pendente para processamento"""
        if not self.notas_pendentes:
            return None
        
        return self.notas_pendentes[0]
    
    def obter_nota_por_indice(self, indice_array: int) -> Optional[Dict]:
        """Obtém uma nota pelo índice do array"""
        if 0 <= indice_array < len(self.notas):
            return self.notas[indice_array]
        return None
    
    def marcar_como_processada(self, indice_array: int, nfse: str, autenticidade: str):
        """Marca uma nota como processada com seus dados"""
        coluna_nfse, coluna_auth = CONFIG_NFE['colunas_processamento']
        
        for nota in self.notas_pendentes:
            if nota['indice_array'] == indice_array:
                # Atualiza os dados originais
                self.notas[indice_array][coluna_nfse] = nfse
                self.notas[indice_array][coluna_auth] = autenticidade
                self.notas[indice_array]['DataProcessamento'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                # Move para processadas
                self.notas_processadas.append({
                    'indice_planilha': nota['indice_planilha'],
                    'indice_array': indice_array,
                    'dados': self.notas[indice_array],
                    'status': 'processada'
                })
                
                # Remove das pendentes
                self.notas_pendentes = [n for n in self.notas_pendentes if n['indice_array'] != indice_array]
                
                logger.info(f"Nota {indice_array} (linha {nota['indice_planilha']}) marcada como processada")
                return True
        
        logger.warning(f"Nota {indice_array} não encontrada nas pendentes")
        return False
    
    def exportar_planilha_atualizada(self, caminho_saida: str = None):
        """Exporta a planilha com os dados atualizados"""
        try:
            if caminho_saida is None:
                caminho_saida = CONFIG_NFE['caminho_planilha']
            
            df = pd.DataFrame(self.notas)
            df.to_excel(caminho_saida, index=False)
            logger.info(f"Planilha exportada para: {caminho_saida}")
            return True
        except Exception as e:
            logger.error(f"Erro ao exportar planilha: {e}")
            return False
    
    def get_resumo(self) -> Dict:
        """Retorna um resumo do status das notas"""
        return {
            'total_notas': len(self.notas),
            'pendentes': len(self.notas_pendentes),
            'processadas': len(self.notas_processadas),
            'percentual': f"{(len(self.notas_processadas) / len(self.notas) * 100):.1f}%" if self.notas else "0%"
        }
    
    def listar_notas_pendentes(self) -> List[Dict]:
        """Lista todas as notas pendentes com informações relevantes"""
        return [{
            'linha_planilha': nota['indice_planilha'],
            'indice_array': nota['indice_array'],
            'data': nota['dados'].get('103', 'N/A'),
            'cliente': nota['dados'].get('Nome', 'N/A'),
            'valor': nota['dados'].get('Valor', 'N/A'),
            'status': 'Pendente'
        } for nota in self.notas_pendentes]
    
    def listar_notas_processadas(self) -> List[Dict]:
        """Lista todas as notas processadas"""
        coluna_nfse = CONFIG_NFE['colunas_processamento'][0]
        return [{
            'linha_planilha': nota['indice_planilha'],
            'indice_array': nota['indice_array'],
            'cliente': nota['dados'].get('Nome', 'N/A'),
            'nfse': nota['dados'].get(coluna_nfse, 'N/A'),
            'status': 'Processada'
        } for nota in self.notas_processadas]
    
    def get_credenciais(self) -> Dict:
        """Retorna as credenciais do sistema NFE"""
        return {
            'url': CONFIG_NFE['url_nfe'],
            'usuario': CONFIG_NFE['usuario'],
            'senha': CONFIG_NFE['senha'],
            'inscricao_municipal': CONFIG_NFE['inscricao_municipal']
        }