from modulo_login_nfe import fazer_login_nfe
from coordenadas import coordenadas
import time

def processo_nfe():
    """Processo completo de NFe"""
    print("📝 AUTOMAÇÃO DE NOTA FISCAL")
    print("=" * 50)

    # Fazer login usando a função do módulo
    driver = fazer_login_nfe()
    if not driver:
        print("❌ Falha no login")
        return
    
    # Aqui viria o processamento das notas fiscais
    print("⚠️ Processamento de notas fiscais não implementado ainda")
    print("⏳ Aguardando 10 segundos para demonstração...")
    time.sleep(10)
    
    # Finalizar
    driver.quit()
    print("🎉 Processo de NFe finalizado")

def menu_principal():
    """Menu principal interativo"""
    print("\n" + "=" * 50)
    print("🤖 SISTEMA DE AUTOMAÇÃO NFE - MENU PRINCIPAL")
    print("=" * 50)
    
    print("1 - Executar automação de NFe")
    print("2 - Testar coordenadas")
    print("3 - Só fazer login")
    print("4 - Sair")
    
    opcao = input("\nDigite sua opção: ")
    
    if opcao == "1":
        processo_nfe()
    elif opcao == "2":
        coordenadas()
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