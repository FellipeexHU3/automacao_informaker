# main.py
import sys
import os
from coordenadas import coordenadas

sys.path.append(os.path.dirname(__file__))

def menu_principal():
    """Menu principal"""
    print("🎯 SISTEMA DE AUTOMAÇÃO NFE")
    print("=" * 50)
    print("1 - Executar automação completa")
    print("2 - Testar planilha")
    print("3 - Testar coordenadas")
    print("4 - Ver detalhes da planilha")
    print("5 - Sair")
    
    return input("\nDigite sua opção: ")

def main():
    while True:
        opcao = menu_principal()
        
        if opcao == "1":
            # Automação completa
            from modules.nfe.nfe_automacao import main as nfe_main
            nfe_main()
            
        elif opcao == "2":
            # Testar planilha
            from modules.nfe.nfe_planilha_teste import testar_planilha
            testar_planilha()
        elif opcao == "3":
            # Testar planilha
            from modules.nfe.nfe_planilha_teste import testar_planilha
            coordenadas()

        elif opcao == "4":
            # Ver detalhes
            from modules.nfe.nfe_planilha_teste import mostrar_detalhes_nota
            from modules.nfe.nfe_config import CONFIG_NFE
            
            linha = input("Número da linha (Enter para todas): ").strip()
            if linha:
                mostrar_detalhes_nota(CONFIG_NFE['caminho_planilha'], int(linha))
            else:
                mostrar_detalhes_nota(CONFIG_NFE['caminho_planilha'])
                
        elif opcao == "5":
            print("👋 Até mais!")
            break
            
        else:
            print("❌ Opção inválida")
        
        input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    main()