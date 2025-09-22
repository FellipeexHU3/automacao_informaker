from modules.planilhas.excel_handler import automacao_completa
from modules.planilhas.modulo_planilhas import selecionar_planilha, ler_planilha_vue, ler_planilha_kryterion, ler_planilha_psi, ler_planilha_scantron
from modules.planilhas.uploader import executar_sequencia_navegacao
from coordenadas import coordenadas
from modules.login.modulo_login import fazer_login

def menu_principal():
    print("\n" + "=" * 50)
    print("🤖 SISTEMA DE AUTOMAÇÃO - MENU PRINCIPAL")
    print("=" * 50)
    
    print("1 - Executar automação completa")
    print("2 - Selecionar planilha manualmente")
    print("3 - Testar leitura de planilhas")
    print("4 - Testar coordenadas")
    print("5 - Sair")
    
    opcao = input("\nDigite sua opção: ")
    
    if opcao == "1":
        automacao_completa()
    elif opcao == "2":
        print(selecionar_planilha())
    elif opcao == "3":
        print(ler_planilha_vue())
        print(ler_planilha_kryterion())
        print(ler_planilha_psi())
        print(ler_planilha_scantron())

    elif opcao == "4":
        coordenadas()
    elif opcao == "5":
        print("👋 Até mais!")
        return False
    else:
        print("❌ Opção inválida")
    
    return True

if __name__ == "__main__":
    while menu_principal():
        pass
