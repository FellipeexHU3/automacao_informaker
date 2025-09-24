# modules/nfe/planilha_tester.py
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
        
        # 👇 VERIFICAR SE A COLUNA DE DATA EXISTE
        if coluna_data_esperada in df.columns:
            print(f"   ✅ Coluna de data encontrada!")
            datas = df[coluna_data_esperada].head(3).tolist()
            print(f"   Primeiras datas: {datas}")
        else:
            print(f"   ❌ Coluna de data NÃO encontrada!")
            
            # Buscar colunas similares
            if tipo_planilha == '103':
                # Para planilha 103, procurar coluna 103
                colunas_data = [col for col in df.columns if '103' in str(col)]
            else:
                # Para planilha 43, procurar colunas com "Data"
                colunas_data = [col for col in df.columns if 'Data' in str(col)]
            
            if colunas_data:
                print(f"   Colunas similares: {colunas_data}")
        
        print(f"   Colunas encontradas: {list(df.columns)}")
        
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
                print(f"   Valores de data_emissao: {nfe_teste.dados['data_emissao'].head(3).tolist()}")
            else:
                print("❌ Normalização falhou - coluna 'data_emissao' não encontrada")
                
            # 👇 NOTAS PROCESSADAS
            print("\n📋 ÚLTIMAS 3 NOTAS PROCESSADAS:")
            print("-" * 50)

            if len(nfe_teste.notas_processadas) > 0:
                ultimas_processadas = nfe_teste.notas_processadas[-3:]
                
                for i, nota in enumerate(ultimas_processadas, 1):
                    dados = nota['dados']
                    print(f"Nota {i}:")
                    print(f"  Linha: {nota['indice_planilha']}")
                    print(f"  Cliente: {dados.get('Nome', 'N/A')}")
                    print(f"  Valor: R$ {dados.get('Valor', 'N/A')}")
                    
                    # Tenta mostrar a data normalizada ou original
                    data = dados.get('data_emissao', 'N/A')
                    print(f"  Data: {data}")
                    
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
                print(f"Linha {i+2}: {linha.get('Nome', 'N/A')} | R$ {linha.get('Valor', 'N/A')} | {status}")
                
    except Exception as e:
        print(f"❌ Erro ao mostrar detalhes: {e}")

if __name__ == "__main__":
    teste_rapido()