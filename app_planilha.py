# app_planilha.py (VERSÃO CORRIGIDA)
from modules.planilhas.modulo_planilhas import selecionar_planilha, ler_planilha_vue, ler_planilha_kryterion, ler_planilha_psi, ler_planilha_scantron
from modules.planilhas.uploader import executar_sequencia_navegacao
from coordenadas import coordenadas
from modules.login.modulo_login import fazer_login

# 👇 REMOVA ESTA LINHA (está causando o erro)
# from modules.planilhas.teste_handlers import testar_novos_handlers

def menu_principal():
    print("\n" + "=" * 50)
    print("🤖 SISTEMA DE AUTOMAÇÃO - MENU PRINCIPAL")
    print("=" * 50)
    
    print("1 - Executar automação completa (SISTEMA TRADICIONAL)")
    print("2 - Executar com NOVOS HANDLERS")  # 👈 Vamos ajustar esta opção
    print("3 - Selecionar planilha manualmente")
    print("4 - Testar leitura de planilhas")
    print("5 - Testar coordenadas")
    print("6 - COMPARAR PLANILHAS KRYTERION")
    print("7 - Sair")
    
    opcao = input("\nDigite sua opção: ")
    
    if opcao == "1":
        try:
            from modules.planilhas.excel_handler import automacao_completa
            automacao_completa(usar_handlers=False)  # Sistema tradicional
        except ImportError as e:
            print(f"❌ Erro: {e}")
            print("🔧 Executando automação manual...")
            executar_automacao_manual()
            
    elif opcao == "2":
        # 👇 OPÇÃO 2 AGORA É SEGURA
        try:
            from modules.planilhas.modulo_planilhas import selecionar_planilha_com_handlers
            selecionar_planilha_com_handlers()
        except ImportError:
            print("❌ Sistema de handlers não disponível")
            print("💡 Use a opção 1 (Sistema Tradicional)")
            
    elif opcao == "3":
        dados = selecionar_planilha()
        if dados:
            print(f"✅ Planilha {dados['tipo']} selecionada: {dados['quantidade']} candidatos")
        else:
            print("❌ Nenhuma planilha selecionada")

    elif opcao == "4":
        # Testar leitura de todas as planilhas
        print("📊 TESTANDO LEITURA DE PLANILHAS:")
        print("VUE:", ler_planilha_vue() is not None)
        print("KRYTERION:", ler_planilha_kryterion() is not None)
        print("PSI:", ler_planilha_psi() is not None)
        print("SCANTRON:", ler_planilha_scantron() is not None)
        
    elif opcao == "5":
        coordenadas()
        
    elif opcao == "6":
        try:
            from modules.planilhas.handlers.comparador_planilhas import executar_comparacao_planilhas
            executar_comparacao_planilhas()
        except ImportError as e:
            print(f"❌ Módulo de comparação não disponível: {e}")
        except Exception as e:
            print(f"❌ Erro ao executar comparação: {e}")
    
    elif opcao == "7":
        print("👋 Até mais!")
        return False
        
    else:
        print("❌ Opção inválida")
    
    return True

def executar_automacao_manual():
    """Executa automação manual se o excel_handler falhar"""
    print("\n🎯 EXECUTANDO AUTOMAÇÃO MANUAL")
    print("=" * 40)
    
    try:
        # 1. SELECIONAR PLANILHA
        print("📋 SELECIONANDO PLANILHA...")
        dados_planilha = selecionar_planilha()
        
        if not dados_planilha:
            print("❌ Nenhuma planilha selecionada")
            return
        
        print(f"\n📊 DADOS DA {dados_planilha['tipo']}:")
        print(f"👥 Candidatos: {dados_planilha['quantidade']}")
        print(f"💰 Valor total: {dados_planilha.get('moeda', 'US$')} {dados_planilha['valor_total']:,.2f}")

        # 2. FAZER LOGIN
        driver = fazer_login()
        if not driver:
            return
        
        # 3. EXECUTAR SEQUÊNCIA DE NAVEGAÇÃO
        executar_sequencia_navegacao(dados_planilha)
        
        # 4. FINALIZAR
        print("🎉 AUTOMAÇÃO CONCLUÍDA COM SUCESSO!")
        print(f"✅ Dados da {dados_planilha['tipo']} enviados")
        
        driver.quit()
        
    except Exception as e:
        print(f"❌ Erro na automação manual: {e}")

if __name__ == "__main__":
    while menu_principal():
        pass