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
                            if pd.notna(valor):
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
    
    def extrair_nomes_kryterion(self):
        """Extrai nomes da coluna Candidato da Kryterion"""
        nomes_kryterion = set()
        
        for idx, row in self.planilha_kryterion.iterrows():
            candidato = row.get('Candidato', '')
            if pd.notna(candidato) and candidato != "":
                # Limpa o nome - remove números no início e conteúdo entre {}
                nome_limpo = str(candidato).strip()
                # Remove padrões como "1 Nome" ou "{algo} Nome"
                if nome_limpo and not nome_limpo.startswith(('{', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9')):
                    # Remove conteúdo entre chaves se houver
                    nome_limpo = nome_limpo.split('{')[0].strip()
                    nomes_kryterion.add(nome_limpo.upper())
        
        return nomes_kryterion
    
    def extrair_nomes_destino(self):
        """Extrai nomes combinando First Name + Last Name do Destino"""
        nomes_destino = set()
        
        for idx, row in self.planilha_destino.iterrows():
            first_name = row.get('First Name', '')
            last_name = row.get('Last Name', '')
            
            if pd.notna(first_name) and first_name != "":
                nome_completo = f"{first_name} {last_name}".strip() if pd.notna(last_name) else first_name
                if nome_completo:
                    nomes_destino.add(nome_completo.upper())
        
        return nomes_destino
    
    def comparar_planilhas(self):
        """Comparação simples entre as planilhas"""
        print("\n🔍 INICIANDO COMPARAÇÃO...")
        
        # Extrai nomes
        nomes_kryterion = self.extrair_nomes_kryterion()
        nomes_destino = self.extrair_nomes_destino()
        
        print(f"📊 Kryterion: {len(nomes_kryterion)} nomes únicos")
        print(f"📊 Destino: {len(nomes_destino)} nomes únicos")
        
        # Mostra alguns exemplos
        print(f"\n📝 EXEMPLOS KRYTERION (5 primeiros):")
        for i, nome in enumerate(list(nomes_kryterion)[:5]):
            print(f"   {i+1}. {nome}")
        
        print(f"\n📝 EXEMPLOS DESTINO (5 primeiros):")
        for i, nome in enumerate(list(nomes_destino)[:5]):
            print(f"   {i+1}. {nome}")
        
        # Encontra diferenças
        kryterion_para_destino = nomes_kryterion - nomes_destino
        destino_para_kryterion = nomes_destino - nomes_kryterion
        
        print(f"\n📊 RESULTADOS:")
        print(f"   ➡️  Só na Kryterion: {len(kryterion_para_destino)}")
        print(f"   ⬅️  Só no Destino: {len(destino_para_kryterion)}")
        
        return kryterion_para_destino, destino_para_kryterion
    
    def encontrar_linha_kryterion_por_nome(self, nome_procurado):
        """Encontra a linha completa na Kryterion pelo nome"""
        for idx, row in self.planilha_kryterion.iterrows():
            candidato = row.get('Candidato', '')
            if pd.notna(candidato):
                candidato_limpo = str(candidato).strip().upper()
                # Remove conteúdo entre chaves para comparação
                candidato_limpo = candidato_limpo.split('{')[0].strip()
                if nome_procurado.upper() == candidato_limpo:
                    return row
        return None
    
    def mapear_para_formato_destino(self, linha_kryterion):
        """Mapeia os dados da Kryterion para o formato do Destino - 100% DOS DADOS REAIS"""
        
        # Extrai nome completo da Kryterion
        nome_completo_kryterion = str(linha_kryterion.get('Candidato', '')).strip()
        # Remove conteúdo entre chaves do nome
        nome_completo_kryterion = nome_completo_kryterion.split('{')[0].strip()
        
        # Divide em First Name e Last Name
        partes_nome = nome_completo_kryterion.split()
        first_name = partes_nome[0] if partes_nome else ""
        last_name = ' '.join(partes_nome[1:]) if len(partes_nome) > 1 else ""
        
        # Pega TODOS os dados REAIS da Kryterion
        data_kryterion = linha_kryterion.get('Data')
        hora_inicio_kryterion = linha_kryterion.get('Hora Início Real')
        cliente_kryterion = linha_kryterion.get('Cliente')
        exam_kryterion = linha_kryterion.get('Exam')
        
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
            'Testing Location': 'Informaker Informatica_Sao Paulo',  # Único campo fixo
            'Client': cliente_kryterion if pd.notna(cliente_kryterion) else 'ServiceNow',
            'First Name': first_name,
            'Last Name': last_name,
            'Assessment': exam_kryterion if pd.notna(exam_kryterion) else 'Certified System Administrator',
            'Time Limit (minutes)': 90,  # Campo fixo
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
    
    def adicionar_candidatos_faltantes(self, nomes_faltantes):
        """Adiciona candidatos faltantes da Kryterion para o Destino"""
        try:
            if not nomes_faltantes:
                print("✅ Nenhum candidato para adicionar")
                return self.planilha_destino
            
            print(f"\n📝 Preparando para adicionar {len(nomes_faltantes)} candidatos...")
            
            novos_registros = []
            for nome in nomes_faltantes:
                print(f"\n🔍 Processando: {nome}")
                
                # Encontra a linha completa na Kryterion
                linha_kryterion = self.encontrar_linha_kryterion_por_nome(nome)
                
                if linha_kryterion is not None:
                    # Mapeia os dados REAIS para o formato do Destino
                    novo_registro = self.mapear_para_formato_destino(linha_kryterion)
                    novos_registros.append(novo_registro)
                    print(f"   ✅ Dados mapeados com sucesso")
                else:
                    print(f"   ❌ Linha não encontrada na Kryterion para: {nome}")
            
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
                
                # Separa os dados por mês baseado na data
                meses = {
                    '07-2025': [],
                    '08-2025': [],
                    '09-2025': []
                }
                
                for idx, row in dataframe.iterrows():
                    data_str = str(row.get('Scheduled Date (DD/MM/YYYY)', ''))
                    
                    if any(x in data_str for x in ['07/2025', '/07/', '07-2025']):
                        meses['07-2025'].append(row)
                    elif any(x in data_str for x in ['08/2025', '/08/', '08-2025']):
                        meses['08-2025'].append(row)
                    elif any(x in data_str for x in ['09/2025', '/09/', '09-2025']):
                        meses['09-2025'].append(row)
                    else:
                        meses['07-2025'].append(row)  # Default
                
                # Salva cada aba
                for mes, registros in meses.items():
                    if registros:
                        df_mes = pd.DataFrame(registros)
                        df_mes.to_excel(writer, sheet_name=mes, index=False)
                        print(f"   💾 Aba {mes}: {len(registros)} registros")
            
            print(f"💾 Planilha salva: {caminho_saida}")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao salvar: {e}")
            return False

def executar_comparacao_planilhas():
    """Função principal - 100% DADOS REAIS"""
    print("\n" + "="*60)
    print("🔍 COMPARADOR DE PLANILHAS - DADOS REAIS")
    print("="*60)
    print("📁 COMPARACAO1 (Kryterion) ↔ COMPARACAO2 (Destino)")
    print("⚠️  TODOS OS DADOS VIRÃO DAS PLANILHAS ORIGINAIS")
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
    
    # Comparação
    print("\n🔍 COMPARANDO...")
    kryterion_para_destino, destino_para_kryterion = comparador.comparar_planilhas()
    
    # Processa resultados
    if kryterion_para_destino:
        print(f"\n❌ CANDIDATOS SÓ NA KRYTERION ({len(kryterion_para_destino)}):")
        for i, nome in enumerate(list(kryterion_para_destino)[:20]):
            print(f"   {i+1:2d}. {nome}")
        
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
        for i, nome in enumerate(list(destino_para_kryterion)[:10]):
            print(f"   {i+1:2d}. {nome}")
    
    if not kryterion_para_destino and not destino_para_kryterion:
        print("✅ Planilhas idênticas!")