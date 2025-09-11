from modulo_login import fazer_login
from modulo_ponto import bater_ponto
from coordenadas import coordenadas
import time

def automacao_ponto():
    """Automação de ponto"""
    print("🤖 AUTOMAÇÃO DE PONTO")
    print("=" * 50)

    # 1. Escolher tipo de ponto
    print("\nEscolha o tipo de ponto:")
    print("1 - Entrada")
    print("2 - Almoço")
    print("3 - Volta do Almoço")
    print("4 - Saída")
    
    opcao = input("\nDigite sua opção: ")
    tipos = {
        "1": "Entrada",
        "2": "Almoco", 
        "3": "Volta",
        "4": "Saida"
    }
    
    if opcao not in tipos:
        print("❌ Opção inválida")
        return
    
    # 2. Fazer login
    driver = fazer_login()
    if not driver:
        print("❌ Falha no login")
        return
    
    # 3. Bater ponto usando a função do módulo
    # OBS: Seu módulo não precisa do driver, só do horário
    bater_ponto(tipos[opcao])
    
    input("Pressione Enter para fechar...")
    # 4. Finalizar
    driver.quit()
    print("🎉 Processo de ponto finalizado")

def menu_principal():
    """Menu principal interativo"""
    print("\n" + "=" * 50)
    print("🤖 SISTEMA DE AUTOMAÇÃO - MENU PRINCIPAL")
    print("=" * 50)
    
    print("1 - Executar automação de ponto")
    print("2 - Testar coordenadas")
    print("3 - Só fazer login")
    print("4 - Sair")
    
    opcao = input("\nDigite sua opção: ")
    
    if opcao == "1":
        automacao_ponto()
    elif opcao == "2":
        coordenadas()
    elif opcao == "3":
        driver = fazer_login()
        if driver:
            input("Pressione Enter para fechar...")
            driver.quit()
    elif opcao == "4":
        print("👋 Até mais!")
        return False
    else:
        print("❌ Opção inválida")
    
    return True

# Execução principal
if __name__ == "__main__":
    while menu_principal():
        pass