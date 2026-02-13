# app_nfe.py (versão melhorada)
import sys
import os
from coordenadas import coordenadas

sys.path.append(os.path.dirname(__file__))

def menu_principal():
    """Menu principal que mostra a planilha selecionada"""
    from modules.nfe.nfe_selecao import get_tipo_planilha
    
    tipo = get_tipo_planilha()  # Isso vai pedir seleção se for a primeira vez
    
    print("🎯 SISTEMA DE AUTOMAÇÃO NFE")
    print("=" * 50)
    print(f"📊 Planilha selecionada: {tipo}")
    print("=" * 50)
    print("1 - Executar automação completa")
    print("2 - Testar planilha")
    print("3 - Ver detalhes da planilha")
    print("4 - Trocar planilha")
    print("5 - Testar com dados controlados")
    print("6 - Sair")

    return input("\nDigite sua opção: ")

def main():
    while True:
        opcao = menu_principal()
        
        if opcao == "1":
            from modules.nfe.nfe_automacao import main as nfe_main
            nfe_main()
            
        elif opcao == "2":
            from modules.nfe.nfe_planilha_teste import testar_planilha
            testar_planilha()
            
        elif opcao == "3":
            from modules.nfe.nfe_planilha_teste import mostrar_detalhes_nota
            from modules.nfe.nfe_selecao import get_caminho_planilha
            
            caminho_planilha = get_caminho_planilha()
            linha = input("Número da linha (Enter para todas): ").strip()
            if linha:
                mostrar_detalhes_nota(caminho_planilha, int(linha))
            else:
                mostrar_detalhes_nota(caminho_planilha)
        
        elif opcao == "4":
            # 👈 NOVA FUNÇÃO: Trocar planilha
            from modules.nfe.nfe_selecao import reset_selecao
            reset_selecao()
            print("🔄 Planilha resetada. Selecione novamente no próximo menu.")

        elif opcao == "5":
            from modules.nfe.nfe_teste_seguro import teste_super_seguro_com_cores
            teste_super_seguro_com_cores()
            print("teste com dados controlados finalizado.")  
            
        elif opcao == "6":
            print("👋 Até mais!")
            break
            
        else:
            print("❌ Opção inválida")
        
        input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    main()