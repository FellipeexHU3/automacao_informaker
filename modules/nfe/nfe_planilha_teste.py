import pandas as pd
from datetime import datetime
import os

def testar_planilha(caminho_planilha=None, tipo_planilha=None):
    """
    Testa a leitura da planilha usando o sistema de seleção global
    """
    print("📊 TESTANDO PLANILHA NFE")
    print("=" * 50)
    
    from .nfe_selecao import get_caminho_planilha, get_tipo_planilha, get_coluna_data
    from .nfe_core import NFE  # 👈 IMPORTAR A CLASSE NFE
    
    if not caminho_planilha:
        caminho_planilha = get_caminho_planilha()
        tipo_planilha = get_tipo_planilha()
    
    if not caminho_planilha or not os.path.exists(caminho_planilha):
        print("❌ Caminho da planilha não encontrado!")
        print(f"   Procurando em: {caminho_planilha}")
        return False
    
    try:
        # Ler planilha
        print(f"📖 Lendo planilha {tipo_planilha}: {caminho_planilha}")
        df = pd.read_excel(caminho_planilha)
        
        # 👇 CONVERTER TODOS OS CABEÇALHOS PARA STRING
        df.columns = [str(col) for col in df.columns]
        
        coluna_data_esperada = get_coluna_data(tipo_planilha)
        
        # Informações básicas
        print(f"✅ Planilha carregada com sucesso!")
        print(f"   Tipo: {tipo_planilha}")
        print(f"   Total de linhas: {len(df)}")
        print(f"   Total de colunas: {len(df.columns)}")
        print(f"   Coluna de data esperada: '{coluna_data_esperada}'")
        
        # 👇 VERIFICAR SE A COLUNA DE DATA EXISTE - CORRIGIDO
        if coluna_data_esperada in df.columns:
            print(f"   ✅ Coluna de data encontrada!")
            
            # DEBUG: Mostrar os valores brutos primeiro
            print(f"   🔍 Valores brutos das primeiras 3 datas:")
            for i in range(min(3, len(df))):
                data_bruta = df[coluna_data_esperada].iloc[i]
                print(f"      Linha {i}: {data_bruta} (tipo: {type(data_bruta)})")
            
            # CORREÇÃO: Converter para datetime ANTES de formatar
            try:
                df[coluna_data_esperada] = pd.to_datetime(df[coluna_data_esperada], errors='coerce', dayfirst=True)
                print("   ✅ Datas convertidas para datetime")
            except Exception as e:
                print(f"   ⚠️  Erro na conversão: {e}")
            
            # Agora formatar as datas corretamente
            datas_formatadas = []
            for i in range(min(3, len(df))):
                data_valor = df[coluna_data_esperada].iloc[i]
                if pd.notna(data_valor) and hasattr(data_valor, 'strftime'):
                    data_formatada = data_valor.strftime('%d/%m/%Y')
                elif pd.notna(data_valor):
                    data_str = str(data_valor)
                    data_formatada = data_str.split()[0] if ' ' in data_str else data_str
                else:
                    data_formatada = 'N/A'
                datas_formatadas.append(data_formatada)
            
            print(f"   📅 Primeiras datas formatadas: {datas_formatadas}")
        else:
            print(f"   ❌ Coluna de data NÃO encontcida!")
            
            # Buscar colunas similares
            if tipo_planilha == '103':
                # Para planilha 103, procurar coluna 103
                colunas_data = [col for col in df.columns if 'Data \nMovimento' in str(col)]
            else:
                # Para planilha 43, procurar colunas com "Data"
                colunas_data = [col for col in df.columns if 'Data' in str(col)]
            
            if colunas_data:
                print(f"   🔍 Colunas similares: {colunas_data}")
        
        print(f"   📋 Colunas encontradas: {list(df.columns)}")
        
        # 👇 VERIFICAÇÃO DE COLUNAS OBRIGATÓRIAS
        colunas_obrigatorias = ['RPS', 'CPF', 'Nome', 'Valor', 'NFSe', 'Autenticidade']
        colunas_faltantes = [col for col in colunas_obrigatorias if col not in df.columns]
        
        if colunas_faltantes:
            print(f"⚠️  Colunas faltantes: {colunas_faltantes}")
        else:
            print("✅ Todas colunas obrigatórias presentes")

        # 👇 TESTAR NORMALIZAÇÃO - AGORA CORRETO
        print("\n🧪 TESTANDO NORMALIZAÇÃO:")
        
        # Criar instância NFE corretamente
        nfe_teste = NFE(caminho_planilha=caminho_planilha, tipo_planilha=tipo_planilha)
        
        if hasattr(nfe_teste, 'dados') and nfe_teste.dados is not None:
            if 'data_emissao' in nfe_teste.dados.columns:
                print("✅ Normalização funcionando - coluna 'data_emissao' criada")
                
                # DEBUG: Verificar o que tem na coluna data_emissao
                print(f"   🔍 Valores brutos de data_emissao:")
                for i in range(min(3, len(nfe_teste.dados))):
                    data_bruta = nfe_teste.dados['data_emissao'].iloc[i]
                    print(f"      Linha {i}: {data_bruta} (tipo: {type(data_bruta)})")
                
                # CORREÇÃO: Formatar datas corretamente
                datas_formatadas = []
                for i in range(min(3, len(nfe_teste.dados))):
                    data_valor = nfe_teste.dados['data_emissao'].iloc[i]
                    if pd.notna(data_valor) and hasattr(data_valor, 'strftime'):
                        data_formatada = data_valor.strftime('%d/%m/%Y')
                    elif pd.notna(data_valor):
                        data_str = str(data_valor)
                        data_formatada = data_str.split()[0] if ' ' in data_str else data_str
                    else:
                        data_formatada = 'N/A'
                    datas_formatadas.append(data_formatada)
                
                print(f"  📅 Valores de data_emissao: {datas_formatadas}")
            else:
                print("❌ Normalização falhou - coluna 'data_emissao' não encontrada")
                
            # 👇 NOTAS PROCESSADAS - CORRIGIDO
            print("\n📋 ÚLTIMAS 3 NOTAS PROCESSADAS:")
            print("-" * 50)

            if len(nfe_teste.notas_processadas) > 0:
                ultimas_processadas = nfe_teste.notas_processadas[-3:]
                
                for i, nota in enumerate(ultimas_processadas, 1):
                    dados = nota['dados']
                    print(f"Nota {i}:")
                    print(f"  Linha: {nota['indice_planilha']}")
                    print(f"  Cliente: {dados.get('Nome', 'N/A')}")
                    valor = dados.get('Valor', 'N/A')
                    valor_formatado = formatar_moeda_br(valor)
                    print(f"  Valor: {valor_formatado}")
                    
                    # CORREÇÃO: Formatar data individual corretamente
                    data = dados.get('data_emissao', 'N/A')
                    if data != 'N/A' and hasattr(data, 'strftime'):
                        data_formatada = data.strftime('%d/%m/%Y')
                    elif data != 'N/A':
                        data_str = str(data)
                        data_formatada = data_str.split()[0] if ' ' in data_str else data_str
                    else:
                        data_formatada = 'N/A'

                    print(f"  Data: {data_formatada}")
                    if tipo_planilha and tipo_planilha.startswith('campinas'):
                        print(f"  NFSe: {dados.get('Nº NF', 'N/A')}")
                        print(f"  Autenticidade: {dados.get('Código', 'N/A')}")
                    else:    
                        print(f"  NFSe: {dados.get('NFSe', 'N/A')}")
                        print(f"  Autenticidade: {dados.get('Autenticidade', 'N/A')}")
                    print()
            else:
                print("📭 Nenhuma nota processada encontrada")

            # 👇 ESTATÍSTICAS
            print(f"\n📈 ESTATÍSTICAS:")
            print(f"   Total de notas: {len(nfe_teste.notas)}")
            print(f"   Notas processadas: {len(nfe_teste.notas_processadas)}")
            print(f"   Notas pendentes: {len(nfe_teste.notas_pendentes)}")
            
            if nfe_teste.notas:
                percentual = (len(nfe_teste.notas_processadas) / len(nfe_teste.notas)) * 100
                print(f"   Percentual concluído: {percentual:.1f}%")
        else:
            print("❌ Falha ao carregar dados no NFE")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao ler planilha: {e}")
        import traceback
        traceback.print_exc()
        return False

def mostrar_detalhes_nota(caminho_planilha, numero_linha=None):
    """
    Mostra detalhes de uma nota específica ou de todas
    """
    
    try:
        df = pd.read_excel(caminho_planilha)
        
        if numero_linha is not None:
            # Mostrar uma linha específica
            if numero_linha < 2 or numero_linha > len(df) + 1:
                print("❌ Número de linha inválido")
                return
            
            linha = df.iloc[numero_linha - 2]  # -2 porque Excel começa na linha 1 + header
            print(f"📄 DETALHES LINHA {numero_linha}:")
            print("-" * 50)
            for coluna, valor in linha.items():
                print(f"  {coluna}: {valor}")
        else:

            


            # Mostrar resumo de todas as linhas
            print("📋 RESUMO DE TODAS AS NOTAS:")
            print("-" * 50)
            for i, linha in df.iterrows():
                status = "✅ PROCESSADA" if pd.notna(linha.get('NFSe')) else "⏳ PENDENTE"
                print(f"Linha {i+2}: {linha.get('Nome', 'N/A')} | {formatar_moeda_br(linha.get('Valor', 'N/A'))} | {status}")
                
    except Exception as e:
        print(f"❌ Erro ao mostrar detalhes: {e}")

def formatar_moeda_br(valor):
    """Formata valor como moeda brasileira R$ 1.000,00"""
    if valor == 'N/A' or valor is None:
        return 'R$ N/A'
    
    try:
        if isinstance(valor, str):
            # Tenta converter string para float
            valor = float(valor.replace(',', '.'))
        
        return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except (ValueError, TypeError):
        return f"R$ {valor}"

def teste_rapido():
    """Função para teste rápido"""
    print("🧪 Teste rápido do planilha_tester")
    testar_planilha()

if __name__ == "__main__":
    teste_rapido()