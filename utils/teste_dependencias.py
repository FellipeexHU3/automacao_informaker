# utils/teste_dependencias.py
"""
MÓDULO DE TESTE DE DEPENDÊNCIAS
Testa todas as dependências do sistema e verifica o ambiente
"""

import sys
import os
import subprocess
import importlib

def verificar_ambiente():
    """Verifica informações do ambiente Python"""
    print("🔍 DIAGNÓSTICO DO AMBIENTE")
    print("=" * 40)
    print(f"🐍 Python executável: {sys.executable}")
    print(f"📁 Diretório atual: {os.getcwd()}")
    print(f"🎯 Virtual env: {os.getenv('VIRTUAL_ENV', 'Não')}")
    print(f"🔧 Versão Python: {sys.version}")
    print()

def teste_dotenv():
    """Testa especificamente o dotenv"""
    print("🧪 TESTE ESPECÍFICO - DOTENV")
    print("=" * 30)
    
    # Teste 1 - Import básico
    try:
        from dotenv import load_dotenv
        print("✅ from dotenv import load_dotenv → OK")
    except ImportError as e:
        print(f"❌ ImportError: {e}")
        print("💡 Tentando instalar automaticamente...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "python-dotenv"])
            from dotenv import load_dotenv
            print("✅ python-dotenv instalado e importado!")
        except Exception as install_error:
            print(f"❌ Falha na instalação: {install_error}")
            return False
    
    # Teste 2 - Função load_dotenv
    try:
        load_dotenv()
        print("✅ load_dotenv() → OK")
    except Exception as e:
        print(f"❌ load_dotenv() failed: {e}")
        return False
    
    # Teste 3 - Verificar variáveis de ambiente
    try:
        import os
        # Testa se consegue acessar variáveis
        test_var = os.getenv('TEST_VAR', 'Valor padrão - variáveis funcionando')
        print(f"✅ Variáveis de ambiente: {test_var}")
        
        # Testa se .env é carregado (crie um arquivo .env de teste se necessário)
        if os.path.exists('.env'):
            print("✅ Arquivo .env encontrado")
        else:
            print("ℹ️  Arquivo .env não encontrado (normal se não existir)")
            
    except Exception as e:
        print(f"❌ os.getenv() failed: {e}")
        return False
    
    print("🎉 dotenv funcionando perfeitamente!")
    return True

def teste_todas_dependencias():
    """Testa todas as dependências do sistema"""
    print("\n📦 TESTE COMPLETO DE DEPENDÊNCIAS")
    print("=" * 40)
    
    dependencias = {
        'pandas': 'pandas',
        'numpy': 'numpy', 
        'pyautogui': 'pyautogui',
        'selenium': 'selenium',
        'webdriver_manager': 'webdriver_manager',
        'dotenv': 'dotenv',
        'openpyxl': 'openpyxl',
        'flask': 'flask',
        'requests': 'requests'
    }
    
    problemas = []
    
    for nome_pip, nome_import in dependencias.items():
        try:
            __import__(nome_import)
            print(f"✅ {nome_pip}")
        except ImportError as e:
            print(f"❌ {nome_pip}")
            problemas.append(nome_pip)
    
    return problemas

def verificar_versoes():
    """Verifica as versões instaladas"""
    print("\n📋 VERSÕES INSTALADAS")
    print("=" * 25)
    
    bibliotecas = ['python-dotenv', 'selenium', 'pandas', 'numpy', 'openpyxl']
    
    for lib in bibliotecas:
        try:
            from importlib.metadata import version
            ver = version(lib)
            print(f"📦 {lib:15} v{ver}")
        except Exception:
            print(f"❌ {lib:15} versão não detectada")

def main():
    """Função principal - teste completo de dependências"""
    print("🚀 INICIANDO TESTE DE DEPENDÊNCIAS")
    print("=" * 50)
    
    # 1. Verifica ambiente
    verificar_ambiente()
    
    # 2. Teste específico do dotenv
    dotenv_ok = teste_dotenv()
    
    # 3. Teste todas as dependências
    problemas = teste_todas_dependencias()
    
    # 4. Verifica versões
    verificar_versoes()
    
    # 5. Resumo
    print("\n" + "=" * 50)
    print("📊 RESUMO DOS TESTES")
    print("=" * 50)
    
    if dotenv_ok and not problemas:
        print("🎉 TODOS OS TESTES PASSARAM!")
        print("✅ dotenv funcionando")
        print("✅ Todas as dependências OK")
    else:
        if not dotenv_ok:
            print("❌ PROBLEMAS COM DOTENV")
        if problemas:
            print(f"❌ DEPENDÊNCIAS FALTANDO: {', '.join(problemas)}")
            print(f"\n💡 PARA INSTALAR: pip install {' '.join(problemas)}")
    
    print("\n⏹️  Teste concluído!")
    input("\n⏸️  Pressione Enter para continuar...")

if __name__ == "__main__":
    main()