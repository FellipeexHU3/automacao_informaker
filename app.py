# app_unificado.py
import os
import sys

def menu_principal():
    print("\n" + "=" * 60)
    print("🤖 SISTEMA DE AUTOMAÇÃO UNIFICADO")
    print("=" * 60)
    print("1 - 📋 AUTOMAÇÃO DE PLANILHAS")
    print("2 - 📄 AUTOMAÇÃO NFE")
    print("3 - 🔐 SISTEMA DE LOGIN")
    print("4 - ⏰ AUTOMAÇÃO DE PONTO")
    print("5 - 📋 UTILS")
    print("6 - 🚪 SAIR")
    print("=" * 60)
    
    opcao = input("\n🎯 Digite sua opção: ").strip()
    
    if opcao == "1":
        executar_automacao_planilhas()
    elif opcao == "2":
        executar_automacao_nfe()
    elif opcao == "3":
        executar_sistema_login()
    elif opcao == "4":
        executar_automacao_ponto()
    elif opcao == "5":
        executar_utils()
    elif opcao == "6":
        print("👋 Até mais! Obrigado por usar o sistema!")
        return False
    else:
        print("❌ Opção inválida! Tente novamente.")
    
    return True

def executar_automacao_planilhas():
    """Executa o sistema de automação de planilhas"""
    print("\n" + "=" * 40)
    print("📋 INICIANDO AUTOMAÇÃO DE PLANILHAS")
    print("=" * 40)
    
    # Importação dentro da função para evitar conflitos
    try:
        from app_planilha import menu_principal as menu_planilhas
        
        # Cria uma versão adaptada do menu
        def menu_adaptado():
            while True:
                if not menu_planilhas():
                    break
        menu_adaptado()
        
    except ImportError as e:
        print(f"❌ Erro ao carregar módulo de planilhas: {e}")
        input("Pressione Enter para continuar...")

def executar_automacao_nfe():
    """Executa o sistema de automação NFE"""
    print("\n" + "=" * 40)
    print("📄 INICIANDO AUTOMAÇÃO NFE")
    print("=" * 40)
    
    try:
        from app_nfe import main as main_nfe
        main_nfe()
    except ImportError as e:
        print(f"❌ Erro ao carregar módulo NFE: {e}")
        input("Pressione Enter para continuar...")

def executar_sistema_login():
    """Executa o sistema de login"""
    print("\n" + "=" * 40)
    print("🔐 INICIANDO SISTEMA DE LOGIN")
    print("=" * 40)
    
    try:
        from app_login import menu_principal as menu_login
        
        # Cria uma versão adaptada do menu
        def menu_adaptado():
            while True:
                if not menu_login():
                    break
        menu_adaptado()
        
    except ImportError as e:
        print(f"❌ Erro ao carregar módulo de login: {e}")
        input("Pressione Enter para continuar...")

def executar_automacao_ponto():
    """Executa o sistema de automação de ponto"""
    print("\n" + "=" * 40)
    print("⏰ INICIANDO AUTOMAÇÃO DE PONTO")
    print("=" * 40)
    
    try:
        from automacao_ponto import menu_principal as menu_ponto
        
        # Cria uma versão adaptada do menu
        def menu_adaptado():
            while True:
                if not menu_ponto():
                    break
        menu_adaptado()
        
    except ImportError as e:
        print(f"❌ Erro ao carregar módulo de ponto: {e}")
        input("Pressione Enter para continuar...")
        
def executar_utils():
    """Executa o sistema utils"""
    print("\n" + "=" * 40)
    print("📋 INICIANDO UTILS")
    print("=" * 40)
    
    # Importação dentro da função para evitar conflitos
    try:
        from app_utils import menu_utils
        
        # Cria uma versão adaptada do menu
        def menu_adaptado():
            while True:
                if not menu_utils():
                    break
        menu_adaptado()
        
    except ImportError as e:
        print(f"❌ Erro ao carregar módulo utils: {e}")
        input("Pressione Enter para continuar...")        

def main():
    """Função principal do sistema unificado"""
    print("🔄 Iniciando Sistema Unificado de Automação...")
    
    while True:
        try:
            if not menu_principal():
                break
        except KeyboardInterrupt:
            print("\n\n⚠️  Interrompido pelo usuário")
            break
        except Exception as e:
            print(f"\n❌ Erro inesperado: {e}")
            input("Pressione Enter para continuar...")

if __name__ == "__main__":
    main()