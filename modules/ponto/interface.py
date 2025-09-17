from .ponto_core import PontoAutomacao
from .config import COORDENADAS_PADRAO, TIPOS_PONTO, NOMES_PONTO
from modules.login.modulo_login import fazer_login 

def automacao_ponto():
    print("🤖 AUTOMAÇÃO DE PONTO")
    print("=" * 50)

    # Escolher tipo de ponto
    print("\nEscolha o tipo de ponto:")
    print("1 - Entrada")
    print("2 - Almoço")
    print("3 - Volta do Almoço")
    print("4 - Saída")
    
    opcao = input("\nDigite sua opção: ")
    
    if opcao not in TIPOS_PONTO:
        print("❌ Opção inválida")
        return
    
    tipo_ponto = TIPOS_PONTO[opcao]
    
    # Fazer login
    driver = fazer_login()
    if not driver:
        print("❌ Falha no login")
        return
    
    try:
        # Inicializar sistema de ponto
        ponto = PontoAutomacao(COORDENADAS_PADRAO)
        
        # Bater ponto
        sucesso = ponto.bater_ponto(tipo_ponto)
        
        if sucesso:
            print(f"✅ {NOMES_PONTO[tipo_ponto]} registrado com sucesso!")
        else:
            print("❌ Falha ao registrar ponto")
            
    finally:
        input("Pressione Enter para fechar...")
        driver.quit()
        print("🎉 Processo finalizado")

def menu_principal():
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
        testar_coordenadas()
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

def testar_coordenadas():
    """Testa as coordenadas configuradas"""
    ponto = PontoAutomacao(COORDENADAS_PADRAO)
    ponto.testar_coordenadas()
    input("Pressione Enter para continuar...")