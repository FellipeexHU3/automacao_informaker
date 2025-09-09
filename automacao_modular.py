from modulo_login import fazer_login
from modulo_planilhas import selecionar_planilha
from modulo_mouse_planilhas import executar_sequencia_navegacao
from coordenadas import coordenadas
import time

def automacao_completa():
    """Automação completa modularizada"""
    print("🤖 AUTOMAÇÃO COMPLETA - SISTEMA MODULAR")
    print("=" * 50)
    
    # 1. SELECIONAR PLANILHA
    print("📋 SELECIONANDO PLANILHA...")
    dados_planilha = selecionar_planilha()
    
    if not dados_planilha:
        print("❌ Nenhuma planilha selecionada")
        return
    
    print(f"\n📊 DADOS DA {dados_planilha['tipo']}:")
    print(f"👥 Candidatos: {dados_planilha['quantidade']}")
    print(f"💰 Valor total: US$ {dados_planilha['valor_total']:,.2f}")

    # 2. FAZER LOGIN
    driver = fazer_login()
    if not driver:
        return
    
    # 3. EXECUTAR SEQUÊNCIA DE NAVEGAÇÃO
    executar_sequencia_navegacao(dados_planilha)
    if not dados_planilha:
        return
    # 6. FINALIZAR
    print("🎉 AUTOMAÇÃO CONCLUÍDA COM SUCESSO!")
    print(f"✅ Dados da {dados_planilha['tipo']} enviados")
    
    driver.quit()

def menu_principal():
    """Menu principal interativo"""
    print("\n" + "=" * 50)
    print("🤖 SISTEMA DE AUTOMAÇÃO - MENU PRINCIPAL")
    print("=" * 50)
    
    print("1 - Executar automação completa")
    print("2 - Selecionar planilha manualmente")
    print("3 - Testar leitura de planilhas")
    print("4 - Só fazer login")
    print("5 - testar coordenadas")
    print("6 - Só executar sequência mouse")
    print("7 - Sair")
    
    opcao = input("\nDigite sua opção: ")
    
    if opcao == "1":
        automacao_completa()
    elif opcao == "2":
            print(selecionar_planilha())
    elif opcao == "3":
        from modulo_planilhas import ler_planilha_vue, ler_planilha_kryterion, ler_planilha_psi
        print("\n📊 TESTANDO PLANILHAS:")
        print(ler_planilha_vue())
        print(ler_planilha_kryterion())
        print(ler_planilha_psi())
    elif opcao == "4":
        driver = fazer_login()
        if driver:
            input("Pressione Enter para fechar...")
            driver.quit()
    elif opcao == "5":
        coordenadas()
    elif opcao == "6":
        executar_sequencia_navegacao()
    elif opcao == "7":
        print("👋 Até mais!")
        return False
    else:
        print("❌ Opção inválida")
    
    return True

# Execução principal
if __name__ == "__main__":
    while menu_principal():
        pass