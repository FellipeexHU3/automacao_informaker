# modules/planilhas/comparador_planilhas.py
import pandas as pd
from pathlib import Path
import shutil
from datetime import datetime
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
        """Normaliza nome para comparação flexível"""
        import unicodedata
        import re
        
        if pd.isna(nome) or nome == "":
            return ""
        
        nome_str = str(nome)
        # Remove conteúdo entre chaves e números no início
        nome_str = re.sub(r'\{.*?\}', '', nome_str)
        nome_str = re.sub(r'^\d+\s*', '', nome_str)
        
        # Remove acentos e converte para maiúsculas
        nome_str = unicodedata.normalize('NFKD', nome_str)
        nome_str = ''.join(c for c in nome_str if not unicodedata.combining(c))
        
        # Remove espaços extras e caracteres especiais
        nome_str = re.sub(r'[^A-Z\s]', '', nome_str.upper())
        nome_str = re.sub(r'\s+', ' ', nome_str).strip()
        
        return nome_str
    
    def normalizar_curso(self, curso):
        """Normaliza nome do curso para comparação flexível - CORRIGIDA"""
        if pd.isna(curso) or curso == "":
            return ""
        
        curso_str = str(curso).upper().strip()
        
        # CORREÇÃO: Remove prefixos comuns incluindo "GOOGLE CLOUD -"
        substituicoes = {
            'GOOGLE CLOUD - ': '',
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
        """Normaliza cliente - CORRIGIDA para tratar espaços"""
        if pd.isna(cliente) or cliente == "":
            return ""
        
        cliente_str = str(cliente).upper().strip()
        # CORREÇÃO: Remove espaços extras
        cliente_str = ' '.join(cliente_str.split())
        return cliente_str
    
    def extrair_chave_kryterion(self, row):
        """Extrai chave única para comparação da Kryterion - VERSÃO COMPLETA"""
        # Filtra apenas Completed e não Waived
        status = row.get('Status', '')
        if pd.isna(status) or str(status).upper() != 'COMPLETED':
            return None
        
        # Verifica se é Waived
        if 'WAIVED' in str(status).upper():
            return None
        
        # Verifica NO SHOW pelas observações
        observacoes = str(row.get('Observações', '')).upper()
        if 'NO SHOW' in observacoes:
            return None
        
        # Verifica NO SHOW pelos horários 00:00
        hora_inicio = str(row.get('Hora Início Real', ''))
        hora_fim = str(row.get('Hora Fim Real', ''))
        if '00:00:00' in hora_inicio and '00:00:00' in hora_fim:
            return None
        
        # Extrai e normaliza dados
        nome = self.normalizar_nome(row.get('Candidato ', ''))
        if not nome:
            return None
        
        curso = self.normalizar_curso(row.get('Exam', ''))
        cliente = self.normalizar_cliente(row.get('Cliente ', ''))
        data = row.get('Data')
        
        if pd.isna(data) or pd.isna(curso):
            return None
        
        # Formata data para YYYY-MM para comparação por MÊS (não dia exato)
        
        
        try:
            if hasattr(data, 'strftime'):
                data_str = data.strftime('%Y-%m')
            else:
                # Tenta converter string como "1-jul-25" para datetime
                data_str_raw = str(data)
                if '-' in data_str_raw:
                    try:
                        # Converte "1-jul-25" para datetime
                        data_obj = datetime.strptime(data_str_raw, '%d-%b-%y')
                        data_str = data_obj.strftime('%Y-%m')
                    except:
                        # Fallback: pega os primeiros 7 caracteres se for formato diferente
                        data_str = data_str_raw[:7]
                    else:
                        data_str = str(data).split()[0][:7]
        except:
            return None
        
        return f"{nome}|{curso}|{cliente}|{data_str}"
    
    def extrair_chave_destino(self, row):
        """Extrai chave única para comparação do Destino - CORRIGIDA"""
        try:
            # Pega os dados básicos
            first_name = str(row.get('First Name', '')).strip()
            last_name = str(row.get('Last Name', '')).strip()
            
            # Verifica se tem pelo menos o primeiro nome
            if not first_name:
                return None
                
            nome = self.normalizar_nome(f"{first_name} {last_name}")
            if not nome:
                return None
            
            curso = self.normalizar_curso(row.get('Assessment', ''))
            cliente = self.normalizar_cliente(row.get('Client', ''))
            data_str = str(row.get('Scheduled Date (DD/MM/YYYY)', ''))
            
            # CORREÇÃO: Verificações mais flexíveis
            if not curso or not cliente or not data_str or data_str == 'nan':
                return None
            
            # CORREÇÃO: Converte data do formato DD/MM/YYYY para YYYY-MM
            try:
                if '/' in data_str:
                    parts = data_str.split('/')
                    if len(parts) == 3:
                        day, month, year = parts
                        # Garante que o ano tenha 4 dígitos
                        if len(year) == 2:
                            year = '20' + year
                        data_iso = f"{year}-{month}"
                    else:
                        return None
                else:
                    return None
            except:
                return None
        
        return f"{nome}|{curso}|{cliente}|{data_iso}"
    
        except Exception as e:
            print(f"❌ Erro ao processar linha do Destino: {e}")
            return None

    def extrair_chave_destino(self, row):
        """Extrai chave única para comparação do Destino - VERSÃO COMPLETA"""
        nome = self.normalizar_nome(f"{row.get('First Name', '')} {row.get('Last Name', '')}")
        if not nome:
            return None
        
        curso = self.normalizar_curso(row.get('Assessment', ''))
        cliente = self.normalizar_cliente(row.get('Client', ''))
        data_str = str(row.get('Scheduled Date (DD/MM/YYYY)', ''))
        
        if not data_str or not curso:
            return None
        
        # Converte data do formato DD/MM/YYYY para YYYY-MM (apenas mês)
        try:
            parts = data_str.split('/')
            if len(parts) == 3:
                data_iso = f"{parts[2]}-{parts[1]}"
            else:
                return None
        except:
            return None
        
        return f"{nome}|{curso}|{cliente}|{data_iso}"
    
    def comparar_planilhas_inteligente(self):
        """Comparação inteligente com matching flexível - VERSÃO COMPLETA"""
        print("\n🔍 INICIANDO COMPARAÇÃO INTELIGENTE...")
        print("   📋 Critérios: Nome + Curso + Cliente + Data")
        print("   ✅ Filtros: Status=Completed, sem NO SHOW, sem Waived")
        
        # Coletar estatísticas para debug
        stats = {
            'kryterion_total': 0,
            'kryterion_validos': 0,
            'destino_total': 0, 
            'destino_validos': 0,
            'matches': 0
        }
        
        # Processar Kryterion
        registros_kryterion = {}
        print(f"\n📊 Processando Kryterion...")
        
        for idx, row in self.planilha_kryterion.iterrows():
            stats['kryterion_total'] += 1
            chave = self.extrair_chave_kryterion(row)
            if chave:
                registros_kryterion[chave] = row
                stats['kryterion_validos'] += 1
        
        # DEBUG: Verificar primeiras linhas do Destino - COLOQUE AQUI
        print(f"\n🔍 DEBUG - ANALISANDO DESTINO:")
        for i in range(min(3, len(self.planilha_destino))):
            row = self.planilha_destino.iloc[i]
            print(f"   Linha {i+1}:")
            print(f"      First Name: '{row.get('First Name', '')}'")
            print(f"      Last Name: '{row.get('Last Name', '')}'")
            print(f"      Assessment: '{row.get('Assessment', '')}'")
            print(f"      Client: '{row.get('Client', '')}'")
            print(f"      Scheduled Date: '{row.get('Scheduled Date (DD/MM/YYYY)', '')}'")
            
            chave = self.extrair_chave_destino(row)
            print(f"      Chave gerada: {chave}")
            print()
        
        # Processar Destino
        registros_destino = {}
        print(f"📊 Processando Destino...")
        
        for idx, row in self.planilha_destino.iterrows():
            stats['destino_total'] += 1
            chave = self.extrair_chave_destino(row)
            if chave:
                registros_destino[chave] = row
                stats['destino_validos'] += 1
        
        # Encontrar matches
        chaves_kryterion = set(registros_kryterion.keys())
        chaves_destino = set(registros_destino.keys())
        
        matches = chaves_kryterion.intersection(chaves_destino)
        stats['matches'] = len(matches)
        
        kryterion_para_destino = chaves_kryterion - chaves_destino
        destino_para_kryterion = chaves_destino - chaves_kryterion
        
        # RESULTADOS
        print(f"\n📊 RESULTADOS:")
        print(f"   ✅ Matches encontrados: {stats['matches']}")
        print(f"   ➡️  Só na Kryterion: {len(kryterion_para_destino)}")
        print(f"   ⬅️  Só no Destino: {len(destino_para_kryterion)}")
        print(f"   📊 Kryterion: {stats['kryterion_validos']}/{stats['kryterion_total']} válidos")
        print(f"   📊 Destino: {stats['destino_validos']}/{stats['destino_total']} válidos")
        
        # DEBUG DETALHADO - Mostrar exemplos reais
        self.mostrar_debug_detalhado(registros_kryterion, registros_destino, matches, kryterion_para_destino)
        
        return kryterion_para_destino, destino_para_kryterion, stats['matches']
    def mostrar_debug_detalhado(self, registros_kryterion, registros_destino, matches, kryterion_para_destino):
        """Mostra debug detalhado do processo de matching"""
        
        # 1. MOSTRAR ALGUNS MATCHES ENCONTRADOS
        if matches:
            print(f"\n🎯 EXEMPLOS DE MATCHES (3 primeiros):")
            for i, chave in enumerate(list(matches)[:3]):
                partes = chave.split('|')
                if len(partes) == 4:
                    nome, curso, cliente, data = partes
                    print(f"   {i+1}. {nome}")
                    
                    # Dados da Kryterion
                    if chave in registros_kryterion:
                        row_k = registros_kryterion[chave]
                        print(f"      Kryterion: {row_k.get('Candidato ', '')} | {row_k.get('Exam', '')} | {row_k.get('Cliente ', '')} | {row_k.get('Data', '')}")
                    
                    # Dados do Destino  
                    if chave in registros_destino:
                        row_d = registros_destino[chave]
                        print(f"      Destino:  {row_d.get('First Name', '')} {row_d.get('Last Name', '')} | {row_d.get('Assessment', '')} | {row_d.get('Client', '')} | {row_d.get('Scheduled Date (DD/MM/YYYY)', '')}")
                    print()
        
        # 2. MOSTRAR CANDIDATOS QUE PRECISAM SER ADICIONADOS
        if kryterion_para_destino:
            print(f"\n📝 CANDIDATOS PARA ADICIONAR (5 primeiros):")
            for i, chave in enumerate(list(kryterion_para_destino)[:5]):
                partes = chave.split('|')
                if len(partes) == 4:
                    nome, curso, cliente, data = partes
                    
                    if chave in registros_kryterion:
                        row_k = registros_kryterion[chave]
                        print(f"   {i+1}. {row_k.get('Candidato ', '')}")
                        print(f"      Curso: {row_k.get('Exam', '')}")
                        print(f"      Cliente: {row_k.get('Cliente ', '')}") 
                        print(f"      Data: {row_k.get('Data', '')}")
                        print(f"      Status: {row_k.get('Status', '')}")
                        print()
        
        # 3. ESTATÍSTICAS DE CLIENTES
        clientes_kryterion = set()
        clientes_destino = set()
        
        for chave in registros_kryterion:
            partes = chave.split('|')
            if len(partes) == 4:
                clientes_kryterion.add(partes[2])
        
        for chave in registros_destino:
            partes = chave.split('|')
            if len(partes) == 4:
                clientes_destino.add(partes[2])
        
        print(f"\n🏢 ESTATÍSTICAS DE CLIENTES:")
        print(f"   Kryterion: {len(clientes_kryterion)} clientes → {sorted(clientes_kryterion)}")
        print(f"   Destino: {len(clientes_destino)} clientes → {sorted(clientes_destino)}")
    
    def encontrar_linha_kryterion_por_chave(self, chave):
        """Encontra a linha na Kryterion pela chave de comparação"""
        for idx, row in self.planilha_kryterion.iterrows():
            chave_atual = self.extrair_chave_kryterion(row)
            if chave_atual == chave:
                return row
        return None
    
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
        
        # Formata data e hora - mantém os valores originais
        data_formatada = self.formatar_data(data_kryterion)
        hora_formatada = self.formatar_hora(hora_inicio_kryterion)
        
        print(f"\n🔍 MAPEANDO DADOS REAIS:")
        print(f"   Nome: {nome_completo_kryterion}")
        print(f"   Data: {data_kryterion} → {data_formatada}")
        print(f"   Hora: {hora_inicio_kryterion} → {hora_formatada}")
        print(f"   Cliente: {cliente_kryterion}")
        print(f"   Exam: {exam_kryterion}")
        
        # Cria registro com dados REAIS
        novo_registro = {
            'Testing Location': 'Informaker Informatica_Sao Paulo',
            'Client': cliente_kryterion,
            'First Name': first_name,
            'Last Name': last_name,
            'Assessment': exam_kryterion,
            'Time Limit (minutes)': 90,
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
    
    def adicionar_candidatos_faltantes(self, chaves_faltantes):
        """Adiciona candidatos faltantes da Kryterion para o Destino"""
        try:
            if not chaves_faltantes:
                print("✅ Nenhum candidato para adicionar")
                return self.planilha_destino
            
            print(f"\n📝 Preparando para adicionar {len(chaves_faltantes)} candidatos...")
            
            novos_registros = []
            for chave in chaves_faltantes:
                partes = chave.split('|')
                if len(partes) == 4:
                    nome, curso, cliente, data = partes
                    print(f"\n🔍 Processando: {nome} | {curso} | {cliente} | {data}")
                
                # Encontra a linha completa na Kryterion
                linha_kryterion = self.encontrar_linha_kryterion_por_chave(chave)
                
                if linha_kryterion is not None:
                    # Mapeia os dados REAIS para o formato do Destino
                    novo_registro = self.mapear_para_formato_destino(linha_kryterion)
                    novos_registros.append(novo_registro)
                    print(f"   ✅ Dados mapeados com sucesso")
                else:
                    print(f"   ❌ Linha não encontrada na Kryterion para: {chave}")
            
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
        """Salva a planilha mantendo a estrutura de abas"""
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
                
                # Separa os dados por mês baseado na data - CORREÇÃO
                meses = {
                    '07-2025': [],
                    '08-2025': [], 
                    '09-2025': []
                }
                
                for idx, row in dataframe.iterrows():
                    data_str = str(row.get('Scheduled Date (DD/MM/YYYY)', ''))
                    
                    # CORREÇÃO: Verificação mais precisa das datas
                    try:
                        # Converte a string de data para objeto datetime
                        if '/' in data_str:
                            day, month, year = data_str.split('/')
                            if len(day) == 2 and len(month) == 2 and len(year) == 4:
                                # Verifica o mês para classificar na aba correta
                                if month == '07':
                                    meses['07-2025'].append(row)
                                elif month == '08':
                                    meses['08-2025'].append(row)
                                elif month == '09':
                                    meses['09-2025'].append(row)
                                else:
                                    # Se for outro mês, classifica pelo ano-mês
                                    meses['07-2025'].append(row)
                            else:
                                meses['07-2025'].append(row)
                        else:
                            meses['07-2025'].append(row)
                    except:
                        meses['07-2025'].append(row)
                
                # Salva cada aba
                for mes, registros in meses.items():
                    if registros:
                        df_mes = pd.DataFrame(registros)
                        df_mes.to_excel(writer, sheet_name=mes, index=False)
                        print(f"   💾 Aba {mes}: {len(registros)} registros")
                    else:
                        # Cria aba vazia para manter a estrutura
                        df_vazio = pd.DataFrame(columns=dataframe.columns)
                        df_vazio.to_excel(writer, sheet_name=mes, index=False)
                        print(f"   💾 Aba {mes}: 0 registros (vazia)")
            
            print(f"💾 Planilha salva: {caminho_saida}")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao salvar: {e}")
            return False

def executar_comparacao_planilhas():
    """Função principal - COMPARAÇÃO INTELIGENTE"""
    print("\n" + "="*60)
    print("🔍 COMPARADOR DE PLANILHAS - COMPARAÇÃO INTELIGENTE")
    print("="*60)
    print("📁 COMPARACAO1 (Kryterion) ↔ COMPARACAO2 (Destino)")
    print("🎯 Critérios: Nome + Curso + Cliente + Data")
    print("✅ Filtros: Completed, sem NO SHOW, sem Waived")
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
    
    # Comparação INTELIGENTE
    print("\n🔍 COMPARANDO...")
    kryterion_para_destino, destino_para_kryterion, matches_encontrados = comparador.comparar_planilhas_inteligente()
    
    # Processa resultados
    if kryterion_para_destino:
        print(f"\n❌ CANDIDATOS VÁLIDOS SÓ NA KRYTERION ({len(kryterion_para_destino)}):")
        for i, chave in enumerate(list(kryterion_para_destino)[:20]):
            partes = chave.split('|')
            if len(partes) == 4:
                nome, curso, cliente, data = partes
                print(f"   {i+1:2d}. {nome} | {curso} | {cliente} | {data}")
        
        if len(kryterion_para_destino) > 20:
            print(f"   ... e mais {len(kryterion_para_destino) - 20}")
        
        # Pergunta se quer adicionar
        adicionar = input("\n📝 Adicionar estes candidatos ao Destino? (s/n): ").lower().strip()
        if adicionar == 's':
            planilha_atualizada = comparador.adicionar_candidatos_faltantes(kryterion_para_destino)
            if planilha_atualizada is not None:
                comparador.salvar_planilha(planilha_atualizada)
                print("🎉 CONCLUÍDO!")
    
    if destino_para_kryterion:
        print(f"\n⚠️  CANDIDATOS SÓ NO DESTINO ({len(destino_para_kryterion)}):")
        print("(Apenas para informação)")
        for i, chave in enumerate(list(destino_para_kryterion)[:10]):
            partes = chave.split('|')
            if len(partes) == 4:
                nome, curso, cliente, data = partes
                print(f"   {i+1:2d}. {nome} | {curso} | {cliente} | {data}")
    
    if not kryterion_para_destino and not destino_para_kryterion:
        print("✅ Planilhas idênticas!")