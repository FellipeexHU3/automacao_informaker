from modules.login.modulo_login_nfe import fazer_login_nfe
from modules.login.modulo_login_vpn import fazer_login_vpn
from modules.login.modulo_login import fazer_login

def menu_principal():
    print("\n" + "=" * 50)
    print("🤖 TESTES DE LOGIN - MENU PRINCIPAL")
    print("=" * 50)
    
    print("1 - LOGIN NA VPN")
    print("2 - LOGIN NO SISTEMA")
    print("3 - LOGIN NFE")
    print("4 - Sair")
    
    opcao = input("\nDigite sua opção: ")
    
    if opcao == "1":
        fazer_login_vpn()
    elif opcao == "2":
        driver = fazer_login()
        if driver:
            input("Pressione Enter para fechar...")
            driver.quit()
    elif opcao == "3":
        driver = fazer_login_nfe()
        if driver:
            input("Pressione Enter para fechar...")
            driver.quit()
    elif opcao == "4":
        print("👋 Até mais!")
        return False
    else:
        print("❌ Opção inválida")
    
    return True

if __name__ == "__main__":
    while menu_principal():
        pass
