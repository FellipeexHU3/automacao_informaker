# modules/nfe/planilha_tester.py
import pandas as pd
from datetime import datetime
import os

def testar_planilha(caminho_planilha=None):
    """
    Testa a leitura da planilha e mostra informações básicas
    """
    print("📊 TESTANDO PLANILHA NFE")
    print("=" * 50)
    
    # Se não informar caminho, tenta pegar do .env
    if not caminho_planilha:
        from .nfe_config import CONFIG_NFE
        caminho_planilha = CONFIG_NFE['caminho_planilha']
    
    if not caminho_planilha or not os.path.exists(caminho_planilha):
        print("❌ Caminho da planilha não encontrado!")
        print(f"   Procurando em: {caminho_planilha}")
        return False
    
    try:
        # Ler planilha
        print(f"📖 Lendo planilha: {caminho_planilha}")
        df = pd.read_excel(caminho_planilha)
        
        # Informações básicas
        print(f"✅ Planilha carregada com sucesso!")
        print(f"   Total de linhas: {len(df)}")
        print(f"   Total de colunas: {len(df.columns)}")
        print(f"   Colunas encontradas: {list(df.columns)}")
        
        # Verificar colunas obrigatórias
        colunas_obrigatorias = ['103', 'CPF', 'Nome', 'Valor', 'NFSe', 'Autenticidade']
        colunas_faltantes = [col for col in colunas_obrigatorias if col not in df.columns]
        
        if colunas_faltantes:
            print(f"⚠️  Colunas faltantes: {colunas_faltantes}")
        else:
            print("✅ Todas colunas obrigatórias presentes")
        

        print("\n📋 ÚLTIMAS 3 NOTAS PROCESSADAS:")
        print("-" * 50)

        # Filtrar apenas as linhas que têm NFSe preenchida
        notas_processadas = df[df['NFSe'].notna()]

        if len(notas_processadas) > 0:
            # Pegar as 3 últimas notas processadas
            ultimas_processadas = notas_processadas.tail(3)
            
            for i, (index, row) in enumerate(ultimas_processadas.iterrows(), 1):
                print(f"Nota {i}:")
                print(f"  Linha: {index + 2}")
                print(f"  Cliente: {row.get('Nome', 'N/A')}")
                print(f"  Valor: R$ {row.get('Valor', 'N/A')}")
                print(f"  NFSe: {int(row.get('NFSe', 'N/A'))}")
                print(f"  Autenticidade: {row.get('Autenticidade', 'N/A')}")
                print()
        else:
            print("📭 Nenhuma nota processada encontrada")

        # Verificar notas pendentes vs processadas
        nfse_preenchidas = df['NFSe'].notna().sum()
        auth_preenchidas = df['Autenticidade'].notna().sum()
        
        print(f"\n📈 ESTATÍSTICAS:")
        print(f"   Notas com NFSe preenchida: {nfse_preenchidas}/{len(df)}")
        print(f"   Notas com Autenticidade preenchida: {auth_preenchidas}/{len(df)}")
        print(f"   Notas pendentes: {len(df) - nfse_preenchidas}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao ler planilha: {e}")
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

# Função para testar rapidamente
def teste_rapido():
    """Teste rápido da planilha"""
    from .nfe_config import CONFIG_NFE
    testar_planilha(CONFIG_NFE['caminho_planilha'])

if __name__ == "__main__":
    teste_rapido()