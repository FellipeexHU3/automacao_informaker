import pandas as pd
import warnings
import os 
from core.config import config 

# ⚠️ Remover warnings chatos do openpyxl
warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')

def ler_planilha_vue():
    return _ler_planilha("VUE", "CAMINHO_PLANILHA_VUE", "COLUNA_VALOR_VUE", "NOME_ABA_VUE")

def ler_planilha_kryterion():
    return _ler_planilha("KRYTERION", "CAMINHO_PLANILHA_KRYTERION", "COLUNA_VALOR_KRYTERION", "NOME_ABA_KRYTERION")

def ler_planilha_psi():
    return _ler_planilha("PSI", "CAMINHO_PLANILHA_PSI", "COLUNA_VALOR_PSI", "NOME_ABA_PSI")

def ler_planilha_scantron():   
    return _ler_planilha("SCANTRON", "CAMINHO_PLANILHA_SCANTRON", "COLUNA_VALOR_SCANTRON", "NOME_ABA_SCANTRON")

def selecionar_planilha():
    """Menu para escolher a planilha a ser usada na automação"""
    print("\n📋 SELECIONE A PLANILHA:")
    print("1 - VUE")
    print("2 - KRYTERION")
    print("3 - PSI")
    print("4 - SCANTRON")
    
    opcao = input("Digite o número da opção: ")

    if opcao == "1":
        dados = ler_planilha_vue()
    elif opcao == "2":
        dados = ler_planilha_kryterion()
    elif opcao == "3":
        dados = ler_planilha_psi()
    elif opcao == "4":
        dados = ler_planilha_scantron()
    else:
        print("❌ Opção inválida")
        return None
    
    # Processamento adicional para tabelas
    if dados and dados.get('tipo') == 'VUE':
        dados = _processar_dados_vue(dados)
    elif dados and dados.get('tipo') == 'KRYTERION':
        dados = _processar_dados_kryterion(dados)
    elif dados and dados.get('tipo') == 'PSI':
        dados = _processar_dados_psi(dados)
    elif dados and dados.get('tipo') == 'SCANTRON':
        dados = _processar_dados_scantron(dados)
    return dados


def _processar_dados_vue(dados_vue):
    """Processa os dados da VUE para formato final"""
    if dados_vue and 'quantidade' in dados_vue:
        dados_vue['comentario'] = _formatar_comentario_vue(dados_vue)
        print("\n🎯 COMENTÁRIO VUE GERADO:")
    return dados_vue

def _processar_dados_kryterion(dados_kryterion):
    """Processa os dados da Kryterion para formato final"""
    if dados_kryterion and 'quantidade' in dados_kryterion:
        print(_gerar_relatorio_kryterion(dados_kryterion))
        dados_kryterion['comentario'] = _formatar_comentario_kryterion(dados_kryterion)
        print("\n🎯 COMENTÁRIO KRYTERION GERADO:")
    return dados_kryterion

def _processar_dados_psi(dados_psi):
    """Processa os dados da PSI para formato final"""
    if dados_psi and 'qtd_selt' in dados_psi:
        dados_psi['comentario'] = _formatar_comentario_psi(dados_psi)
        print("\n🎯 COMENTÁRIO PSI GERADO:")
    return dados_psi

def _processar_dados_scantron(dados_scantron): 
    """Processa os dados da Scantron para formato final"""
    if dados_scantron and 'quantidade' in dados_scantron:
        dados_scantron['comentario'] = _formatar_comentario_scantron(dados_scantron)
        print("\n🎯 COMENTÁRIO SCANTRON GERADO:")
    return dados_scantron

def _gerar_relatorio_psi(dados_psi):
    """Gera relatório formatado para PSI"""
    return f"""
    📊 RELATÓRIO PSI DETALHADO
    ==========================
    👥 TOTAL GERAL: {dados_psi['quantidade']} candidatos
    🔵 SELT: {dados_psi.get('qtd_selt', 0)} candidatos  
    🔴 Outros: {dados_psi.get('qtd_outros', 0)} candidatos
    💰 VALOR TOTAL: {dados_psi['moeda']} {dados_psi['valor_total']:,.2f}

    📈 ESTATÍSTICAS:
    • SELT: {(dados_psi.get('qtd_selt', 0)/dados_psi['quantidade']*100):.1f}%
    • Outros: {(dados_psi.get('qtd_outros', 0)/dados_psi['quantidade']*100):.1f}%
    """

def _gerar_relatorio_vue(dados_vue, relatorio_detalhado):
    """Gera um relatório detalhado formatado para VUE"""
    relatorio = []
    relatorio.append("\n📋 RELATÓRIO COMPLETO - VUE")
    relatorio.append("=" * 60)
    
    # Detalhamento por cliente
    relatorio.append("📊 DISTRIBUIÇÃO POR CLIENTE:")
    for item in relatorio_detalhado:
        relatorio.append(f"   • {item['cliente']}: {item['quantidade']} provas ({item['percentual']:.1f}%)")
    
    relatorio.append("-" * 40)
    relatorio.append(f"👥 TOTAL GERAL: {dados_vue['quantidade']} provas")

    return "\n".join(relatorio)

def _gerar_relatorio_kryterion(dados_kryterion):
    """Gera relatório detalhado do Kryterion por mês"""
    if not dados_kryterion or "valores_por_aba" not in dados_kryterion:
        return "❌ Dados inválidos para relatório Kryterion"
    
    total_candidatos = dados_kryterion['quantidade']
    total_valor = dados_kryterion['valor_total']
    moeda = dados_kryterion.get("moeda", "US$")
    
    relatorio = [
        "📊 RELATÓRIO KRYTERION DETALHADO",
        "==========================",
        f"👥 TOTAL GERAL: {total_candidatos} candidatos",
        f"💰 VALOR TOTAL: {moeda} {total_valor:,.2f}",
        "",
        "📈 DETALHES POR MÊS:"
    ]
    
    for aba, valores in dados_kryterion["valores_por_aba"].items():
        qtd = valores["quantidade"]
        val = valores["valor_total"]
        
        perc_qtd = (qtd / total_candidatos * 100) if total_candidatos > 0 else 0
        perc_val = (val / total_valor * 100) if total_valor > 0 else 0
        
        relatorio.append(
            f"\n📋 {aba}:"
            f"\n   👥 Candidatos: {qtd} ({perc_qtd:.1f}%)"
            f"\n   💵 Valor: {moeda} {val:,.2f} ({perc_val:.1f}%)"
        )
    
    return "\n".join(relatorio)


def _formatar_comentario_vue(dados_vue):
    """Formata o comentário para a textbox da VUE"""
    return f""" ID: 23098
    PEARSON VUE
    Site ID: #88405
    Candidates - {dados_vue.get('quantidade', 0):02d}"""


def _formatar_comentario_kryterion(dados_kryterion):
    """Formata o comentário para a textbox da Kryterion"""
    return f"""ID: 23167
    KRYTERION
    3T (JUL - AGO - SET)
    Candidates - {dados_kryterion.get('quantidade', 0):02d}"""

def _formatar_comentario_psi(dados_psi):
    """Formata o comentário para a textbox da PSI"""
    return f"""ID 23157
    PSI SITE #12693 - {dados_psi.get('qtd_outros', 0):02d} Candidates
    PSI SITE #12807 (SELT) - {dados_psi.get('qtd_selt', 0):02d} Candidates"""


def _formatar_comentario_scantron(dados_scantron):
    """Formata o comentário para a textbox da Scantron"""
    return f""" ID: 23168
    MEAZURE Learning
    Center ID: #10932
    Candidates -7 {dados_scantron.get('quantidade', 0):02d}"""


def _ler_planilha(nome, caminho_env, coluna_env, aba_env, header=0):
    """Função genérica para ler uma planilha e extrair informações."""
    caminho = getattr(config, caminho_env, None)
    coluna_valor = getattr(config, coluna_env, None)
    nome_aba = getattr(config, aba_env, None)

    if not caminho or not os.path.exists(caminho):
        print(f"❌ Arquivo não encontrado: {caminho}")
        return None

    try:
          # Mostrar abas disponíveis (FORA DO IF, PARA TODAS AS PLANILHAS)
        excel_file = pd.ExcelFile(caminho)
        print(f"\n📊 PROCESSANDO {nome}:")
        print(f"✅ Abas disponíveis: {excel_file.sheet_names}")

       # ⚠️ CASO ESPECIAL KRYTERION - PROCESSAR TODAS AS ABAS (Mês 1, Mês 2, Mês 3)
        if nome == "KRYTERION":
            abas_alvo = ["Mês 1", "Mês 2", "Mês 3"]
            total_geral = 0
            valor_total_geral = 0.0
            abas_processadas = []
            
            for aba in abas_alvo:
                if aba in excel_file.sheet_names:
                    print(f"\n📋 PROCESSANDO ABA: {aba}")
                    
                    # Ler cada aba com header=1
                    df_aba = pd.read_excel(caminho, sheet_name=aba, header=1)
                    print(f"✅ Estrutura da {aba}: {list(df_aba.columns)}")
                    
                    if coluna_valor and coluna_valor in df_aba.columns:
                        valores_validos = df_aba[coluna_valor].notna().sum()
                        valor_aba = df_aba[coluna_valor].sum()
                        
                        total_geral += valores_validos
                        valor_total_geral += valor_aba
                        abas_processadas.append(aba)
                        
                        print(f"✅ Coluna '{coluna_valor}' encontrada!")
                        print(f"💰 Valores não nulos em {aba}: {valores_validos}")
                        print(f"💵 Valor total em {aba}: {valor_aba:.2f}")
                    else:
                        print(f"❌ Coluna '{coluna_valor}' NÃO encontrada na aba {aba}!")
                        continue
                else:
                    print(f"⚠️ Aba '{aba}' não encontrada")
            
            if not abas_processadas:
                print("❌ Nenhuma aba válida processada")
                return None
            
            print(f"\n🎯 TOTAL GERAL KRYTERION:")
            print(f"   📊 Total de registros: {total_geral}")
            print(f"   💰 Valor total: {valor_total_geral:.2f}")
            print(f"   📋 Abas processadas: {', '.join(abas_processadas)}")
            
            # Dados de retorno para Kryterion
            valores_por_aba = {}

            for aba in abas_alvo:
                if aba in excel_file.sheet_names:
                    df_aba = pd.read_excel(caminho, sheet_name=aba, header=1)
                    if coluna_valor and coluna_valor in df_aba.columns:
                        valores_validos = df_aba[coluna_valor].notna().sum()
                        valor_aba = df_aba[coluna_valor].sum()
                        valores_por_aba[aba] = {
                            "quantidade": int(valores_validos),
                            "valor_total": float(valor_aba)
                        }

            retorno = {
                "tipo": nome,
                "quantidade": int(total_geral),
                "valor_total": float(valor_total_geral),
                "abas_processadas": abas_processadas,
                "valores_por_aba": valores_por_aba,
                "moeda": "US$"
            }

        if nome == "SCANTRON":
            df = pd.read_excel(caminho, sheet_name=nome_aba if nome_aba else 0, header=1)
            print(f"✅ Estrutura: {list(df.columns)}")

            # Verificar coluna de valor
            valor_total = 0.0
            if coluna_valor and coluna_valor in df.columns:
                valores_validos = df[coluna_valor].notna().sum()
                valor_total = df[coluna_valor].sum()
                print(f"✅ Coluna '{coluna_valor}' encontrada!")
                print(f"💰 Quantidade de Candidatos: {valores_validos}")
                print(f"💵 Valor total: {valor_total:.2f}")
            else:
                print(f"❌ Coluna '{coluna_valor}' NÃO encontrada!")
                return None

            # Dados base de retorno para outras planilhas
            retorno = {
                "tipo": nome,
                "quantidade": int(len(df)),
                "valor_total": float(valor_total),
                "moeda": "US$"
            }
        
        if nome == "VUE":
            df = pd.read_excel(caminho, sheet_name=nome_aba if nome_aba else 0, header=0)
            valor_total = 0.0
            if 'Cliente ' in df.columns:
                # Limpar e filtrar dados
                clientes_validos = df["Cliente "].dropna().astype(str)
                valor_total = df[coluna_valor].sum()
                
                # Contagem por cliente
                contagem_clientes = clientes_validos.value_counts()
                total_geral = len(clientes_validos)
                
                print(f"👥 RELATÓRIO DETALHADO - CLIENTES VUE:")
                print("=" * 50)
                
                relatorio_detalhado = []
                
                # Gerar relatório para cada cliente
                for cliente, quantidade in contagem_clientes.items():
                    percentual = (quantidade / total_geral) * 100
                    print(f"   📊 {cliente}: {percentual:.1f}% - {quantidade} provas")
                    relatorio_detalhado.append({
                        'cliente': cliente,
                        'quantidade': quantidade,
                        'percentual': percentual
                    })
                retorno = {
                    "tipo": nome,
                    "quantidade": int(len(df)),
                    "valor_total": float(valor_total),
                    "moeda": "US$"
                }
                print("=" * 50)
                
                # Gerar relatório formatado
                print(_gerar_relatorio_vue(retorno, relatorio_detalhado))
                    
            else:
                print("⚠️ Coluna 'Cliente' não encontrada para análise VUE")
                    # 🔎 CASO ESPECIAL PSI - Contar SELT vs Outros

        if nome == "PSI":
            df = pd.read_excel(caminho, sheet_name=nome_aba if nome_aba else 0, header=0)
            valor_total = 0.0
            # Verificar se tem coluna 'Cliente' para identificar SELT
            if 'Cliente ' in df.columns:
                valor_total = df[coluna_valor].sum()
                clientes_validos = df["Cliente "].dropna().astype(str)
                qtd_selt = clientes_validos.str.contains("selt", case=False, na=False).sum()
                qtd_outros = len(clientes_validos) - qtd_selt

                total_geral = qtd_selt + qtd_outros

                print(f"👥 CLIENTES PSI:")
                print(f"   ✅ SELT: {qtd_selt}")
                print(f"   ✅ Outros: {qtd_outros}")
                print(f"   ✅ TOTAL GERAL: {total_geral}")

                retorno = {
                    "tipo": nome,
                    "quantidade": int(len(df)),
                    "valor_total": float(valor_total),
                    "moeda": "US$"
                }
                # Atualizar quantidade para o total real de candidatos
                retorno["quantidade"] = int(total_geral)
                retorno["qtd_selt"] = int(qtd_selt)
                retorno["qtd_outros"] = int(qtd_outros)
                print(_gerar_relatorio_psi(retorno))             
            else:
                print("⚠️ Coluna 'Cliente' não encontrada para análise PSI")

        return retorno  # ✅ Retorna apenas dados brutos, sem relatório

    except Exception as e:
        print(f"❌ Erro ao processar {nome}: {e}")
        return None


def selecionar_tipo_planilha():
    """Apenas seleciona o tipo da planilha (para testes)"""
    print("\n📋 SELECIONE O TIPO DA PLANILHA:")
    print("1 - VUE")
    print("2 - KRYTERION") 
    print("3 - PSI")
    print("4 - SCANTRON")

    opcao = input("Digite o número: ")
    
    if opcao == "1":
        return 'VUE'
    elif opcao == "2":
        return 'KRYTERION'
    elif opcao == "3":
        return 'PSI'
    elif opcao == "4":
        return 'SCANTRON'
    else:
        print("❌ Opção inválida")
        return None


# === NOVO SISTEMA DE HANDLERS - ADICIONE NO FINAL DO ARQUIVO ===

def selecionar_planilha_com_handlers():
    """
    Versão nova que usa handlers - compatível com o sistema antigo
    """
    print("📋 SELECIONAR PLANILHA - SISTEMA ATUALIZADO (HANDLERS)")
    print("=" * 50)
    
    try:
        # Import dos handlers (com tratamento de erro)
        try:
            from modules.planilhas.handlers.planilha_factory import PlanilhaFactory
        except ImportError as e:
            print(f"❌ Sistema de handlers não disponível: {e}")
            print("🔄 Voltando para sistema tradicional...")
            return selecionar_planilha()  # Fallback para sistema antigo
        
        # Usa a mesma seleção de tipo do sistema antigo
        tipo_selecionado = selecionar_tipo_planilha()
        if not tipo_selecionado:
            return None
        
        # Pega o caminho do config (igual ao sistema antigo)
        mapeamento_caminhos = {
            'VUE': getattr(config, "CAMINHO_PLANILHA_VUE", None),
            'KRYTERION': getattr(config, "CAMINHO_PLANILHA_KRYTERION", None),
            'PSI': getattr(config, "CAMINHO_PLANILHA_PSI", None),
            'SCANTRON': getattr(config, "CAMINHO_PLANILHA_SCANTRON", None)
        }
        
        caminho = mapeamento_caminhos.get(tipo_selecionado)
        if not caminho or not os.path.exists(caminho):
            print(f"❌ Arquivo não encontrado: {caminho}")
            return None
        
        print(f"✅ Processando {tipo_selecionado} com handlers...")
        
        # Processa com handler
        dados = PlanilhaFactory.processar_planilha_completa(caminho, tipo_selecionado.lower())
        
        if dados:
            print(f"✅ Planilha {tipo_selecionado} processada com handlers!")
            
            # Aplica o mesmo processamento do sistema antigo
            if tipo_selecionado == 'VUE':
                dados = _processar_dados_vue(dados)
            elif tipo_selecionado == 'KRYTERION':
                dados = _processar_dados_kryterion(dados)
            elif tipo_selecionado == 'PSI':
                dados = _processar_dados_psi(dados)
            elif tipo_selecionado == 'SCANTRON':
                dados = _processar_dados_scantron(dados)
            
            return dados
        else:
            print("❌ Falha no processamento com handlers")
            return None
        
    except Exception as e:
        print(f"❌ Erro no sistema de handlers: {e}")
        print("🔄 Voltando para sistema tradicional...")
        return selecionar_planilha()  # Fallback

def selecionar_planilha_hibrido(usar_handlers=False):
    """
    Função principal hibrida - escolhe entre sistema antigo e novo
    """
    if usar_handlers:
        return selecionar_planilha_com_handlers()
    else:
        return selecionar_planilha()  # Seu sistema antigo