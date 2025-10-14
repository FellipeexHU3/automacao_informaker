from utils.teste_dependencias import (
    verificar_ambiente,
    teste_dotenv, 
    teste_todas_dependencias,
    verificar_versoes,
    main as teste_dependencias_main
)

def menu_utils():
    """Menu de utilitários do sistema"""
    while True:
        print("\n" + "=" * 50)
        print("🛠️  UTILS - FERRAMENTAS DO SISTEMA")
        print("=" * 50)
        print("1 - 📍 TESTAR COORDENADAS")
        print("2 - 🔍 VERIFICAR DEPENDÊNCIAS")
        print("3 - 📊 VERIFICAR MÓDULOS INTERNOS")
        print("4 - 🧪 TESTES RÁPIDOS DO SISTEMA")
        print("5 - 🐍 DIAGNÓSTICO COMPLETO")
        print("6 - ⬅️  VOLTAR AO MENU PRINCIPAL")
        
        opcao = input("\n🎯 Digite sua opção: ").strip()
        
        if opcao == "1":
            utils_coordenadas()
        elif opcao == "2":
            teste_dependencias_main()  # Teste completo de dependências
        elif opcao == "3":
            utils_verificar_modulos_internos()
        elif opcao == "4":
            utils_testes_rapidos()
        elif opcao == "5":
            utils_diagnostico_completo()
        elif opcao == "6":
            break
        else:
            print("❌ Opção inválida!")

# ============================================================
# 🛠️ FUNÇÕES UTILS (apenas as básicas)
# ============================================================

def utils_coordenadas():
    """Testa as coordenadas do sistema"""
    print("\n📍 INICIANDO TESTE DE COORDENADAS")
    print("=" * 35)
    
    try:
        from utils.coordenadas import coordenadas
        coordenadas()
        print("✅ Teste de coordenadas concluído!")
    except ImportError as e:
        print(f"❌ Erro ao importar coordenadas: {e}")
    except Exception as e:
        print(f"❌ Erro durante teste de coordenadas: {e}")
    
    input("\n⏸️  Pressione Enter para continuar...")

def utils_verificar_modulos_internos():
    """Verifica os módulos internos do sistema"""
    import importlib
    
    print("\n📊 VERIFICANDO MÓDULOS INTERNOS")
    print("=" * 40)
    
    modulos_internos = {
        'modules.planilhas.modulo_planilhas': 'Módulo principal de planilhas',
        'modules.planilhas.uploader': 'Upload de planilhas',
        'modules.login.modulo_login': 'Sistema de login',
        'modules.login.modulo_login_nfe': 'Login NFE',
        'modules.login.modulo_login_vpn': 'Login VPN',
        'utils.coordenadas': 'Configuração de coordenadas'
    }
    
    problemas = []
    
    for modulo, descricao in modulos_internos.items():
        try:
            importlib.import_module(modulo)
            print(f"✅ {modulo:35} - {descricao}")
        except ImportError as e:
            print(f"❌ {modulo:35} - {descricao}")
            print(f"   └── ERRO: {e}")
            problemas.append(modulo)
    
    print("\n" + "=" * 40)
    if problemas:
        print(f"❌ {len(problemas)} MÓDULOS COM PROBLEMAS")
    else:
        print("✅ TODOS OS MÓDULOS ESTÃO OK!")
    
    input("\n⏸️  Pressione Enter para continuar...")

def utils_testes_rapidos():
    """Executa testes rápidos do sistema"""
    import importlib
    
    print("\n🧪 EXECUTANDO TESTES RÁPIDOS")
    print("=" * 35)
    
    testes = [
        ("Importação básica do pandas", "pandas"),
        ("Importação básica do selenium", "selenium"),
        ("Sistema de coordenadas", "utils.coordenadas")
    ]
    
    for descricao, modulo in testes:
        try:
            importlib.import_module(modulo)
            print(f"✅ {descricao}")
        except Exception as e:
            print(f"❌ {descricao}")
            print(f"   └── ERRO: {e}")
    
    print("\n🎯 TESTES CONCLUÍDOS")
    input("\n⏸️  Pressione Enter para continuar...")

def utils_diagnostico_completo():
    """Diagnóstico completo do sistema"""
    print("\n🐍 DIAGNÓSTICO COMPLETO DO SISTEMA")
    print("=" * 45)
    
    # Verifica ambiente
    verificar_ambiente()
    
    # Teste dotenv
    teste_dotenv()
    
    # Teste todas dependências
    teste_todas_dependencias()
    
    # Verifica versões
    verificar_versoes()
    
    input("\n⏸️  Pressione Enter para continuar...")

if __name__ == "__main__":
    menu_utils()