# modules/planilhas/comparador_planilhas.py
import pandas as pd
from pathlib import Path
import shutil
from datetime import datetime
import unicodedata
import re
import logging
from difflib import SequenceMatcher
from core.config import config

class ComparadorPlanilhasKryterion:
    def __init__(self):
        self.planilha_kryterion = None
        self.planilha_destino = None
        self.caminho_destino_original = None
        
    def criar_backup(self, caminho_arquivo):
        """Cria um backup do arquivo antes de modificar"""
        try:
            if not Path(caminho_arquivo).exists():
                print(f"❌ Arquivo não encontrado para backup: {caminho_arquivo}")
                return False
            
            pasta_backups = Path(caminho_arquivo).parent / "backups"
            pasta_backups.mkdir(exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_arquivo = Path(caminho_arquivo).stem
            extensao = Path(caminho_arquivo).suffix
            caminho_backup = pasta_backups / f"{nome_arquivo}_backup_{timestamp}{extensao}"
            
            shutil.copy2(caminho_arquivo, caminho_backup)
            print(f"💾 Backup criado: {caminho_backup}")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao criar backup: {e}")
            return False
    
    def carregar_planilha_kryterion(self):
        """Carrega a planilha da Kryterion (COMPARACAO1) do config"""
        try:
            caminho_planilha = config.CAMINHO_PLANILHA_DESTINO_COMPARACAO1
            
            if not caminho_planilha or not Path(caminho_planilha).exists():
                print(f"❌ Caminho da Kryterion (COMPARACAO1) inválido: {caminho_planilha}")
                return False
            
            print(f"📥 Carregando Kryterion: {Path(caminho_planilha).name}")
            
            # Lê todas as abas (Mês 1, Mês 2, Mês 3)
            xl = pd.ExcelFile(caminho_planilha)
            dfs_kryterion = []
            
            for sheet_name in xl.sheet_names:
                if any(mes in sheet_name for mes in ['Mês 1', 'Mês 2', 'Mês 3']):
                    df = pd.read_excel(caminho_planilha, sheet_name=sheet_name, header=1)
                    print(f"   📑 Aba {sheet_name}: {len(df)} registros")
                    
                    # Mostra estrutura completa para debug
                    print(f"   📊 Colunas encontradas: {list(df.columns)}")
                    
                    if not df.empty:
                        print(f"   👀 Exemplo de dados (primeira linha):")
                        primeira_linha = df.iloc[0]
                        for coluna, valor in primeira_linha.items():
                            if pd.notna(valor) and coluna != 'Observações':
                                print(f"      {coluna}: {valor}")
                    
                    dfs_kryterion.append(df)
            
            if dfs_kryterion:
                self.planilha_kryterion = pd.concat(dfs_kryterion, ignore_index=True)
                print(f"✅ Kryterion carregada: {len(self.planilha_kryterion)} registros totais")
                return True
            else:
                print("❌ Nenhuma aba válida encontrada na planilha Kryterion")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao carregar Kryterion: {e}")
            return False
    
    def carregar_planilha_destino(self):
        """Carrega a planilha de destino (COMPARACAO2) do config"""
        try:
            caminho_planilha = config.CAMINHO_PLANILHA_DESTINO_COMPARACAO2
            
            if not caminho_planilha or not Path(caminho_planilha).exists():
                print(f"❌ Caminho da planilha destino (COMPARACAO2) inválido: {caminho_planilha}")
                return False
            
            self.caminho_destino_original = caminho_planilha
            print(f"📥 Carregando destino: {Path(caminho_planilha).name}")
            
            # Lê todas as abas (07-2025, 08-2025, 09-2025)
            xl = pd.ExcelFile(caminho_planilha)
            dfs_destino = []
            
            for sheet_name in xl.sheet_names:
                if any(mes in sheet_name for mes in ['07-2025', '08-2025', '09-2025']):
                    df = pd.read_excel(caminho_planilha, sheet_name=sheet_name)
                    print(f"   📑 Aba {sheet_name}: {len(df)} registros")
                    
                    # Mostra estrutura completa para debug
                    print(f"   📊 Colunas encontradas: {list(df.columns)}")
                    
                    dfs_destino.append(df)
            
            if dfs_destino:
                self.planilha_destino = pd.concat(dfs_destino, ignore_index=True)
                print(f"✅ Planilha destino carregada: {len(self.planilha_destino)} registros totais")
                return True
            else:
                print("❌ Nenhuma aba válida encontrada na planilha destino")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao carregar planilha destino: {e}")
            return False
    
    def normalizar_nome(self, nome):
        """Normaliza nome para comparação flexível - VERSÃO MELHORADA"""
        if pd.isna(nome) or nome == "":
            return ""
        
        nome_str = str(nome)
        
        # Remove conteúdo entre chaves (mantém números e caracteres normais)
        nome_str = re.sub(r'\{.*?\}', '', nome_str)
        
        # Remove acentos e converte para maiúsculas
        nome_str = unicodedata.normalize('NFKD', nome_str)
        nome_str = ''.join(c for c in nome_str if not unicodedata.combining(c))
        
        # Remove espaços extras e converte para maiúsculas
        nome_str = re.sub(r'\s+', ' ', nome_str).strip().upper()
        
        return nome_str
    
    def normalizar_curso(self, curso):
        """Normaliza nome do curso para comparação flexível - VERSÃO MELHORADA"""
        if pd.isna(curso) or curso == "":
            return ""
        
        curso_str = str(curso).upper().strip()
        
        # Remove prefixos comuns
        substituicoes = {
            'GOOGLE CLOUD - ': '',
            'GOOGLE CLOUD CERTIFIED - ': '',
            'CERTIFIED ': '',
            'CERTIFICATE ': '',
            'CERTIFICATION ': '',
            'PROFESSIONAL ': '',
            'ASSOCIATE ': '',
            'SPECIALIST ': '',
            '(ENGLISH)': '',
            '(PORTUGUESE)': '',
            'PORTUGUESE': '',
            'ENGLISH': '',
            ' - ': ' ',
            '&': 'AND',
            '  ': ' '
        }
        
        for old, new in substituicoes.items():
            curso_str = curso_str.replace(old, new)
        
        # Remove palavras comuns muito curtas
        palavras = curso_str.split()
        palavras_filtradas = [p for p in palavras if len(p) > 2]
        curso_str = ' '.join(palavras_filtradas)
            
        return curso_str.strip()

    def normalizar_cliente(self, cliente):
        """Normaliza cliente"""
        if pd.isna(cliente) or cliente == "":
            return ""
        
        cliente_str = str(cliente).upper().strip()
        cliente_str = ' '.join(cliente_str.split())
        return cliente_str
    
    def comparar_nomes_flexivel(self, nome1, nome2):
        """Compara nomes de forma flexível, permitindo middle names ausentes - VERSÃO REFORÇADA"""
        if pd.isna(nome1) or pd.isna(nome2) or nome1 == "" or nome2 == "":
            return False
        
        nome1_clean = self.normalizar_nome(nome1)
        nome2_clean = self.normalizar_nome(nome2)
        
        # DEBUG: Mostrar o que está sendo comparado
        print(f"      🔍 Comparando nomes: '{nome1}' ↔ '{nome2}'")
        print(f"      🔍 Após normalização: '{nome1_clean}' ↔ '{nome2_clean}'")
        
        # Se já são iguais após normalização, perfeito!
        if nome1_clean == nome2_clean:
            print(f"      ✅ Nomes idênticos após normalização")
            return True
        
        # Divide em partes
        partes1 = nome1_clean.split()
        partes2 = nome2_clean.split()
        
        print(f"      🔍 Partes: {partes1} ↔ {partes2}")
        
        # CASO 1: Um nome tem middle names, o outro não (ex: "Allan Santos" vs "Allan Rodrigo Dei Tosi dos Santos")
        if len(partes1) == 2 and len(partes2) > 2:
            # Verifica se primeiro e último nome coincidem
            if partes1[0] == partes2[0] and partes1[1] == partes2[-1]:
                print(f"      🔄 Nomes flexíveis (abreviado vs completo): {nome1} ↔ {nome2}")
                return True
        
        elif len(partes1) > 2 and len(partes2) == 2:
            # Verifica se primeiro e último nome coincidem
            if partes1[0] == partes2[0] and partes1[-1] == partes2[1]:
                print(f"      🔄 Nomes flexíveis (completo vs abreviado): {nome1} ↔ {nome2}")
                return True
        
        # CASO 2: Ambos têm mais de 2 partes, mas primeiro e último coincidem
        if len(partes1) > 2 and len(partes2) > 2:
            if partes1[0] == partes2[0] and partes1[-1] == partes2[-1]:
                print(f"      🔄 Nomes flexíveis (primeiro+último iguais): {nome1} ↔ {nome2}")
                return True
        
        # CASO 3: Verifica similaridade com fuzzy matching (fallback)
        try:
            similaridade = SequenceMatcher(None, nome1_clean, nome2_clean).ratio()
            print(f"      🔄 Similaridade: {similaridade:.1%}")
            if similaridade > 0.6:  # 60% de similaridade (mais flexível)
                print(f"      🔄 Nomes similares ({similaridade:.1%}): {nome1} ↔ {nome2}")
                return True
        except Exception as e:
            print(f"      ⚠️  Erro no fuzzy matching: {e}")
        
        print(f"      ❌ Nomes não compatíveis")
        return False

    def comparar_cursos_flexivel(self, curso1, curso2):
        """Compara nomes de cursos de forma flexível, permitindo variações"""
        if pd.isna(curso1) or pd.isna(curso2) or curso1 == "" or curso2 == "":
            return False
        
        curso1_norm = self.normalizar_curso(curso1)
        curso2_norm = self.normalizar_curso(curso2)
        
        # DEBUG: Mostrar o que está sendo comparado
        print(f"      🔍 Comparando cursos: '{curso1}' ↔ '{curso2}'")
        print(f"      🔍 Após normalização: '{curso1_norm}' ↔ '{curso2_norm}'")
        
        # Se já são iguais após normalização, perfeito!
        if curso1_norm == curso2_norm:
            print(f"      ✅ Cursos idênticos após normalização")
            return True
        
        # Verifica se um curso está contido no outro
        if curso1_norm in curso2_norm or curso2_norm in curso1_norm:
            print(f"   🔄 Cursos similares: '{curso1}' ↔ '{curso2}'")
            return True
        
        # Remove palavras muito comuns e compara novamente
        palavras_comuns = {'CLOUD', 'CERTIFIED', 'ASSOCIATE', 'PROFESSIONAL', 'ENGINEER', 'ARCHITECT', 'DATA', 'DEVELOPER'}
        
        palavras1 = set(curso1_norm.split()) - palavras_comuns
        palavras2 = set(curso2_norm.split()) - palavras_comuns
        
        # Se as palavras principais coincidem
        if palavras1 and palavras2 and palavras1 == palavras2:
            print(f"   🔄 Cursos com palavras-chave iguais: '{curso1}' ↔ '{curso2}'")
            return True
        
        # Verifica similaridade com fuzzy matching
        try:
            similaridade = SequenceMatcher(None, curso1_norm, curso2_norm).ratio()
            if similaridade > 0.7:  # 70% de similaridade
                print(f"   🔄 Cursos similares ({similaridade:.1%}): '{curso1}' ↔ '{curso2}'")
                return True
        except:
            pass
        
        return False

    def mapear_duracao_prova(self, duracao_kryterion):
        """Mapeia a duração da prova da Kryterion para o formato Destino"""
        if pd.isna(duracao_kryterion) or duracao_kryterion == "":
            return 90  # Valor padrão
        
        duracao_str = str(duracao_kryterion).strip()
        
        print(f"🔍 Processando duração: '{duracao_str}'")  # DEBUG
        
        # Verificação por string - mais robusta
        duracao_lower = duracao_str.lower()
        
        # Procura por padrões específicos nos textos
        if '0,5 a 1,9' in duracao_lower or '30 a 114' in duracao_lower or '90' in duracao_str:
            print(f"   ✅ Mapeado para 90 minutos")
            return 90
        
        elif '2,0 a 2,9' in duracao_lower or '120 a 174' in duracao_lower or '120' in duracao_str:
            print(f"   ✅ Mapeado para 120 minutos") 
            return 120
        
        elif '3,0 a 3,9' in duracao_lower or '180 a 234' in duracao_lower or '180' in duracao_str:
            print(f"   ✅ Mapeado para 180 minutos")
            return 180
        
        # Fallback: tenta extrair números dos parênteses
        elif '(' in duracao_str and 'min' in duracao_lower:
            try:
                # Extrai o conteúdo entre parênteses
                inicio = duracao_str.find('(') + 1
                fim = duracao_str.find(')')
                if inicio > 0 and fim > inicio:
                    conteudo_parenteses = duracao_str[inicio:fim]
                    # Procura pelo primeiro número antes de "a" ou espaço
                    if 'a' in conteudo_parenteses:
                        primeiro_numero = conteudo_parenteses.split('a')[0].strip()
                        minutos = int(primeiro_numero)
                        print(f"   ✅ Extraído dos parênteses: {minutos} minutos")
                        return minutos
            except:
                pass
        
        # Fallback genérico baseado em números encontrados
        try:
            # Procura por qualquer número na string
            numeros = re.findall(r'\d+', duracao_str)
            if numeros:
                maior_numero = max(map(int, numeros))
                if maior_numero <= 114:
                    print(f"   ✅ Número encontrado {maior_numero} → 90 minutos")
                    return 90
                elif maior_numero <= 174:
                    print(f"   ✅ Número encontrado {maior_numero} → 120 minutos")
                    return 120
                else:
                    print(f"   ✅ Número encontrado {maior_numero} → 180 minutos")
                    return 180
        except:
            pass
        
        print(f"   ⚠️  Usando valor padrão 90 minutos")
        return 90  # Valor padrão final
    
    def criar_chave_unica_flexivel(self, row, origem='kryterion'):
        """Cria chave única para comparação flexível - VERSÃO FLEXÍVEL"""
        try:
            if origem == 'kryterion':
                # Filtra apenas Completed e não Waived
                status = row.get('Status', '')
                if pd.isna(status) or str(status).upper() != 'COMPLETED':
                    return None
                
                if 'WAIVED' in str(status).upper():
                    return None
                
                # Verifica NO SHOW
                observacoes = str(row.get('Observações', '')).upper()
                if 'NO SHOW' in observacoes:
                    return None
                
                # Verifica NO SHOW pelos horários 00:00
                hora_inicio = str(row.get('Hora Início Real', ''))
                hora_fim = str(row.get('Hora Fim Real', ''))
                if '00:00:00' in hora_inicio and '00:00:00' in hora_fim:
                    return None
                
                # Extrai dados da Kryterion
                nome_completo = str(row.get('Candidato ', '')).split('{')[0].strip()
                curso = str(row.get('Exam', ''))
                cliente = str(row.get('Cliente ', ''))
                data = row.get('Data')
                
            else:  # origem == 'destino'
                # Extrai dados do Destino
                first_name = str(row.get('First Name', '')).strip()
                last_name = str(row.get('Last Name', '')).strip()
                nome_completo = f"{first_name} {last_name}".strip()
                curso = str(row.get('Assessment', ''))
                cliente = str(row.get('Client', ''))
                data = row.get('Scheduled Date (DD/MM/YYYY)', '')
            
            # Valida dados obrigatórios
            if not nome_completo or not curso or pd.isna(data):
                return None
            
            # Normaliza dados básicos
            cliente_normalizado = self.normalizar_cliente(cliente)
            
            # Processa data de forma robusta
            data_mes = self.extrair_mes_ano(data)
            if not data_mes:
                return None
            
            # Para comparação flexível, usamos apenas cliente + data como chave base
            # Nome e curso serão comparados de forma flexível depois
            chave_base = f"{cliente_normalizado}|{data_mes}"
            
            return {
                'chave_base': chave_base,
                'nome_completo': nome_completo,
                'curso': curso,
                'cliente': cliente,
                'data': data,
                'row_data': row,
                'origem': origem
            }
            
        except Exception as e:
            print(f"❌ Erro ao criar chave flexível ({origem}): {e}")
            return None
    
    def extrair_mes_ano(self, data):
        """Extrai mês e ano de forma robusta de diferentes formatos de data"""
        if pd.isna(data):
            return None
        
        try:
            # Se já é datetime
            if hasattr(data, 'strftime'):
                return data.strftime('%Y-%m')
            
            data_str = str(data)
            
            # Formato YYYY-MM-DD HH:MM:SS
            if '-' in data_str and ':' in data_str:
                try:
                    data_part = data_str.split()[0]
                    data_obj = datetime.strptime(data_part, '%Y-%m-%d')
                    return data_obj.strftime('%Y-%m')
                except:
                    pass
            
            # Formato DD/MM/YYYY
            elif '/' in data_str:
                try:
                    parts = data_str.split('/')
                    if len(parts) == 3:
                        day, month, year = parts
                        if len(year) == 2:
                            year = '20' + year
                        return f"{year}-{month.zfill(2)}"
                except:
                    pass
            
            # Formato DD-MMM-YY (01-JAN-25)
            elif '-' in data_str and len(data_str.split('-')) == 3:
                try:
                    data_obj = datetime.strptime(data_str, '%d-%b-%y')
                    return data_obj.strftime('%Y-%m')
                except:
                    pass
            
            # Tenta parse genérico
            try:
                data_obj = pd.to_datetime(data_str)
                return data_obj.strftime('%Y-%m')
            except:
                return None
                
        except Exception as e:
            print(f"❌ Erro ao processar data '{data}': {e}")
            return None

    def comparar_planilhas_inteligente_flexivel(self):
        """Comparação inteligente com MATCHING FLEXÍVEL DE NOMES E CURSOS"""
        print("\n🔍 INICIANDO COMPARAÇÃO INTELIGENTE COM MATCHING FLEXÍVEL...")
        print("   📋 Critérios: Cliente + Data + Curso (flexível) + Nome (flexível)")
        print("   ✅ Filtros: Status=Completed, sem NO SHOW, sem Waived")
        print("   🔄 Matching: Permite variações em cursos e nomes")
        
        # Coletar estatísticas
        stats = {
            'kryterion_total': 0,
            'kryterion_validos': 0,
            'destino_total': 0, 
            'destino_validos': 0,
            'matches': 0
        }
        
        # Processar Kryterion em grupos
        grupos_kryterion = {}
        print(f"\n📊 Processando Kryterion...")
        
        for idx, row in self.planilha_kryterion.iterrows():
            stats['kryterion_total'] += 1
            chave_info = self.criar_chave_unica_flexivel(row, 'kryterion')
            if chave_info:
                chave_base = chave_info['chave_base']
                if chave_base not in grupos_kryterion:
                    grupos_kryterion[chave_base] = []
                grupos_kryterion[chave_base].append(chave_info)
                stats['kryterion_validos'] += 1
        
        # Processar Destino em grupos
        grupos_destino = {}
        print(f"📊 Processando Destino...")
        
        for idx, row in self.planilha_destino.iterrows():
            stats['destino_total'] += 1
            chave_info = self.criar_chave_unica_flexivel(row, 'destino')
            if chave_info:
                chave_base = chave_info['chave_base']
                if chave_base not in grupos_destino:
                    grupos_destino[chave_base] = []
                grupos_destino[chave_base].append(chave_info)
                stats['destino_validos'] += 1
        
        # COMPARAÇÃO FLEXÍVEL DENTRO DOS GRUPOS
        matches_encontrados = 0
        kryterion_sem_match = []  # Lista de registros da Kryterion sem match
        destino_sem_match = []    # Lista de registros do Destino sem match
        
        print(f"\n🔍 REALIZANDO MATCHING FLEXÍVEL POR GRUPO...")
        
        # Para cada grupo (cliente + data)
        for chave_base in set(list(grupos_kryterion.keys()) + list(grupos_destino.keys())):
            registros_k = grupos_kryterion.get(chave_base, [])
            registros_d = grupos_destino.get(chave_base, [])
            
            # DEBUG: Mostrar o grupo se houver registros em ambas as planilhas
            if registros_k and registros_d:
                print(f"\n   🔍 Grupo: {chave_base}")
                print(f"      Kryterion: {len(registros_k)} registros")
                for r in registros_k:
                    print(f"        👤 {r['nome_completo']} | 📚 {r['curso']}")
                print(f"      Destino: {len(registros_d)} registros")
                for r in registros_d:
                    print(f"        👤 {r['nome_completo']} | 📚 {r['curso']}")
            
            # Marcar registros que foram matched
            matched_k = [False] * len(registros_k)
            matched_d = [False] * len(registros_d)
            
            # Tentar matching para cada registro da Kryterion com cada registro do Destino
            for i, reg_k in enumerate(registros_k):
                for j, reg_d in enumerate(registros_d):
                    if not matched_d[j] and not matched_k[i]:
                        # VERIFICAÇÃO DUPLA FLEXÍVEL: curso E nome
                        cursos_compativeis = self.comparar_cursos_flexivel(reg_k['curso'], reg_d['curso'])
                        nomes_compativeis = self.comparar_nomes_flexivel(reg_k['nome_completo'], reg_d['nome_completo'])
                        
                        if cursos_compativeis and nomes_compativeis:
                            matches_encontrados += 1
                            matched_k[i] = True
                            matched_d[j] = True
                            print(f"      ✅ MATCH FLEXÍVEL: {reg_k['nome_completo']} | {reg_k['curso']}")
                            break
            
            # Após processar o grupo, coletar os registros não matched
            for i, matched in enumerate(matched_k):
                if not matched:
                    kryterion_sem_match.append(registros_k[i])
            
            for j, matched in enumerate(matched_d):
                if not matched:
                    destino_sem_match.append(registros_d[j])
        
        # Estatísticas
        print(f"\n📊 Estatísticas de processamento:")
        print(f"   Kryterion: {stats['kryterion_validos']}/{stats['kryterion_total']} válidos")
        print(f"   Destino: {stats['destino_validos']}/{stats['destino_total']} válidos")
        
        # RESULTADOS
        print(f"\n📊 RESULTADOS COM MATCHING FLEXÍVEL:")
        print(f"   ✅ Matches encontrados: {matches_encontrados}")
        print(f"   ➡️  Só na Kryterion: {len(kryterion_sem_match)}")
        print(f"   ⬅️  Só no Destino: {len(destino_sem_match)}")
        
        return kryterion_sem_match, destino_sem_match, matches_encontrados

    def mostrar_debug_detalhado_flexivel(self, kryterion_sem_match, destino_sem_match, matches_encontrados):
        """Mostra debug detalhado do processo de matching flexível"""
        
        if kryterion_sem_match:
            print(f"\n📝 CANDIDATOS PARA ADICIONAR (5 primeiros):")
            for i, reg_info in enumerate(kryterion_sem_match[:5]):
                print(f"   {i+1}. {reg_info['nome_completo']}")
                print(f"      Curso: {reg_info['curso']}")
                print(f"      Cliente: {reg_info['cliente']}") 
                print(f"      Data: {reg_info['data']}")
                print()

    def encontrar_linha_kryterion_por_info(self, reg_info):
        """Encontra a linha na Kryterion pelas informações do registro"""
        # Já temos a linha no row_data, mas vamos verificar para segurança
        return reg_info['row_data']
    
    def mapear_para_formato_destino(self, linha_kryterion):
        """Mapeia os dados da Kryterion para o formato do Destino - 100% DOS DADOS REAIS"""
        
        # Extrai nome completo da Kryterion
        nome_completo_kryterion = str(linha_kryterion.get('Candidato ', '')).strip()
        # Remove conteúdo entre chaves do nome
        nome_completo_kryterion = nome_completo_kryterion.split('{')[0].strip()
        
        # Divide em First Name e Last Name
        partes_nome = nome_completo_kryterion.split()
        first_name = partes_nome[0] if partes_nome else ""
        last_name = ' '.join(partes_nome[1:]) if len(partes_nome) > 1 else ""
        
        # Pega TODOS os dados REAIS da Kryterion
        data_kryterion = linha_kryterion.get('Data')
        hora_inicio_kryterion = linha_kryterion.get('Hora Início Real')
        cliente_kryterion = linha_kryterion.get('Cliente ', '')
        exam_kryterion = linha_kryterion.get('Exam', '')
        duracao_kryterion = linha_kryterion.get('Duração Prevista', '')
        
        # Mapeia a duração corretamente
        duracao_minutos = self.mapear_duracao_prova(duracao_kryterion)
        
        # Formata data e hora - mantém os valores originais
        data_formatada = self.formatar_data(data_kryterion)
        hora_formatada = self.formatar_hora(hora_inicio_kryterion)
        
        print(f"\n🔍 MAPEANDO DADOS REAIS:")
        print(f"   Nome: {nome_completo_kryterion}")
        print(f"   Data: {data_kryterion} → {data_formatada}")
        print(f"   Hora: {hora_inicio_kryterion} → {hora_formatada}")
        print(f"   Cliente: {cliente_kryterion}")
        print(f"   Exam: {exam_kryterion}")
        print(f"   Duração Kryterion: '{duracao_kryterion}' → {duracao_minutos} minutos")
        
        # Cria registro com dados REAIS
        novo_registro = {
            'Testing Location': 'Informaker Informatica_Sao Paulo',
            'Client': cliente_kryterion,
            'First Name': first_name,
            'Last Name': last_name,
            'Assessment': exam_kryterion,
            'Time Limit (minutes)': duracao_minutos,
            'Scheduled Date (DD/MM/YYYY)': data_formatada,
            'Scheduled Time': hora_formatada,
        }
        
        return novo_registro
    
    def formatar_data(self, data):
        """Formata data mantendo o valor original"""
        if pd.isna(data):
            return ""
        
        try:
            if isinstance(data, str):
                return data
            elif hasattr(data, 'strftime'):
                return data.strftime('%d/%m/%Y')
            else:
                return str(data)
        except:
            return ""
    
    def formatar_hora(self, hora):
        """Formata hora mantendo o valor original"""
        if pd.isna(hora):
            return ""
        
        try:
            if isinstance(hora, str):
                return hora
            elif hasattr(hora, 'strftime'):
                return hora.strftime('%H:%M:%S')
            else:
                return str(hora)
        except:
            return ""
    
    def adicionar_candidatos_faltantes_flexivel(self, registros_faltantes):
        """Adiciona candidatos faltantes da Kryterion para o Destino - VERSÃO FLEXÍVEL"""
        try:
            if not registros_faltantes:
                print("✅ Nenhum candidato para adicionar")
                return self.planilha_destino
            
            print(f"\n📝 Preparando para adicionar {len(registros_faltantes)} candidatos...")
            
            novos_registros = []
            for reg_info in registros_faltantes:
                print(f"\n🔍 Processando: {reg_info['nome_completo']} | {reg_info['curso']} | {reg_info['cliente']} | {reg_info['data']}")
                
                # Usa a linha diretamente do row_data
                linha_kryterion = reg_info['row_data']
                
                if linha_kryterion is not None:
                    # Mapeia os dados REAIS para o formato do Destino
                    novo_registro = self.mapear_para_formato_destino(linha_kryterion)
                    novos_registros.append(novo_registro)
                    print(f"   ✅ Dados mapeados com sucesso")
                else:
                    print(f"   ❌ Linha não encontrada na Kryterion")
            
            if novos_registros:
                df_novos = pd.DataFrame(novos_registros)
                planilha_atualizada = pd.concat([self.planilha_destino, df_novos], ignore_index=True)
                print(f"\n🎉 {len(df_novos)} candidatos preparados para adicionar!")
                return planilha_atualizada
            else:
                print("❌ Nenhum dado válido para adicionar")
                return self.planilha_destino
            
        except Exception as e:
            print(f"❌ Erro ao adicionar candidatos: {e}")
            return None
    
    def salvar_planilha(self, dataframe, caminho_saida=None):
        """Salva a planilha mantendo a estrutura de abas CORRETAMENTE"""
        try:
            if caminho_saida is None:
                caminho_saida = self.caminho_destino_original
            
            # Backup
            print("\n🔒 CRIANDO BACKUP...")
            if not self.criar_backup(self.caminho_destino_original):
                confirmar = input("⚠️  Backup falhou. Continuar? (s/n): ").lower()
                if confirmar != 's':
                    return False
            
            # Salva organizando por meses nas abas
            with pd.ExcelWriter(caminho_saida, engine='openpyxl') as writer:
                
                # Separa os dados por mês baseado na data
                meses = {
                    '07-2025': [],
                    '08-2025': [], 
                    '09-2025': []
                }
                
                for idx, row in dataframe.iterrows():
                    data_str = str(row.get('Scheduled Date (DD/MM/YYYY)', ''))
                    mes_ano = self.extrair_mes_ano(data_str)
                    
                    if mes_ano:
                        mes_aba = f"{mes_ano.split('-')[1]}-{mes_ano.split('-')[0]}"
                        if mes_aba in meses:
                            meses[mes_aba].append(row)
                        else:
                            meses['07-2025'].append(row)
                    else:
                        meses['07-2025'].append(row)
                
                # DEBUG: Mostrar quantos registros em cada aba
                print(f"\n📊 DISTRIBUIÇÃO POR ABAS:")
                for mes, registros in meses.items():
                    print(f"   📑 {mes}: {len(registros)} registros")
                
                # Salva cada aba
                for mes, registros in meses.items():
                    if registros:
                        df_mes = pd.DataFrame(registros)
                        
                        # Garante a ordem das colunas
                        colunas_originais = ['Testing Location', 'Client', 'First Name', 'Last Name', 
                                            'Assessment', 'Time Limit (minutes)', 
                                            'Scheduled Date (DD/MM/YYYY)', 'Scheduled Time']
                        
                        # Mantém apenas as colunas que existem no DataFrame
                        colunas_existentes = [col for col in colunas_originais if col in df_mes.columns]
                        df_mes = df_mes[colunas_existentes]
                        
                        df_mes.to_excel(writer, sheet_name=mes, index=False)
                        print(f"   💾 Aba {mes}: {len(registros)} registros salvo")
                    else:
                        # Cria aba vazia para manter a estrutura
                        df_vazio = pd.DataFrame(columns=dataframe.columns)
                        df_vazio.to_excel(writer, sheet_name=mes, index=False)
                        print(f"   💾 Aba {mes}: 0 registros (vazia)")
                
                print(f"🎯 TOTAL: {len(dataframe)} registros distribuídos")
            
            print(f"💾 Planilha salva: {caminho_saida}")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao salvar: {e}")
            return False

def executar_comparacao_planilhas_flexivel():
    """Função principal - COMPARAÇÃO INTELIGENTE COM MATCHING FLEXÍVEL"""
    print("\n" + "="*60)
    print("🔍 COMPARADOR DE PLANILHAS - COMPARAÇÃO FLEXÍVEL")
    print("="*60)
    print("📁 COMPARACAO1 (Kryterion) ↔ COMPARACAO2 (Destino)")
    print("🎯 Critérios: Cliente + Data + Curso (flexível) + Nome (flexível)")
    print("✅ Filtros: Completed, sem NO SHOW, sem Waived")
    print("🔄 Matching: Permite variações em cursos e nomes")
    print("="*60)
    
    comparador = ComparadorPlanilhasKryterion()
    
    # Carrega planilhas
    print("\n📥 CARREGANDO PLANILHAS...")
    
    if not comparador.carregar_planilha_kryterion():
        print("❌ Falha ao carregar Kryterion")
        return
    
    if not comparador.carregar_planilha_destino():
        print("❌ Falha ao carregar Destino")
        return
    
    # Comparação INTELIGENTE FLEXÍVEL
    print("\n🔍 COMPARANDO COM MATCHING FLEXÍVEL...")
    kryterion_sem_match, destino_sem_match, matches_encontrados = comparador.comparar_planilhas_inteligente_flexivel()
    
    # Processa resultados
    if kryterion_sem_match:
        print(f"\n❌ CANDIDATOS VÁLIDOS SÓ NA KRYTERION ({len(kryterion_sem_match)}):")
        for i, reg_info in enumerate(kryterion_sem_match[:20]):
            print(f"   {i+1:2d}. {reg_info['nome_completo']} | {reg_info['curso']} | {reg_info['cliente']} | {reg_info['data']}")
        
        if len(kryterion_sem_match) > 20:
            print(f"   ... e mais {len(kryterion_sem_match) - 20}")
        
        # Pergunta se quer adicionar
        adicionar = input("\n📝 Adicionar estes candidatos ao Destino? (s/n): ").lower().strip()
        if adicionar == 's':
            planilha_atualizada = comparador.adicionar_candidatos_faltantes_flexivel(kryterion_sem_match)
            if planilha_atualizada is not None:
                comparador.salvar_planilha(planilha_atualizada)
                print("🎉 CONCLUÍDO!")
    
    if destino_sem_match:
        print(f"\n⚠️  CANDIDATOS SÓ NO DESTINO ({len(destino_sem_match)}):")
        print("(Apenas para informação)")
        for i, reg_info in enumerate(destino_sem_match[:50]):
            print(f"   {i+1:2d}. {reg_info['nome_completo']} | {reg_info['curso']} | {reg_info['cliente']} | {reg_info['data']}")
    
    if not kryterion_sem_match and not destino_sem_match:
        print("✅ Planilhas idênticas!")

# Mantém a função original para compatibilidade, mas recomendo usar a nova
def executar_comparacao_planilhas():
    """Função principal legada - usa a nova versão flexível por padrão"""
    print("⚠️  Usando versão legada. Recomendo usar executar_comparacao_planilhas_flexivel()")
    executar_comparacao_planilhas_flexivel()