import pyautogui
import time
from dotenv import load_dotenv  
import os
from .excel_handler import obter_caminho_planilha

# Carregar variáveis do .env uma vez no início
load_dotenv() 
def executar_sequencia_navegacao(dados_planilha):
    """Executa sequência de navegação até o formulário"""
    print("🖱️ EXECUTANDO SEQUÊNCIA DE NAVEGAÇÃO...")
    
    pyautogui.FAILSAFE = True
    try:
        time.sleep(3)
        print("🖱️ PRIMEIRO CLICK - Agendamentos")
        pyautogui.click(22, 210)
        time.sleep(1.5)

        print("🖱️ SEGUNDO CLICK - Schedules") 
        pyautogui.click(22, 230)
        time.sleep(3)

        print("🖱️ TERCEIRO CLICK - Formulário")
        pyautogui.click(230, 280)
        time.sleep(1)
        
        # ⚠️ AGORA DIGITA O NOME DA PLANILHA BASEADO NO TIPO
        print(f"⌨️ Digitando nome da planilha: {dados_planilha['tipo']}")
        if dados_planilha['tipo'] == "VUE":
            pyautogui.write("VUE")# Nome correto para VUE
        elif dados_planilha['tipo'] == "Kryterion":
            pyautogui.write("Kryterion")  # Nome correto para Kryterion
        elif dados_planilha['tipo'] == "PSI":
            pyautogui.write("PSI")       # Nome correto para PSI
        else:
            pyautogui.write(dados_planilha['tipo']) # Usa o próprio tipo como fallback
        time.sleep(0.5)

        print("🖱️ QUARTO CLICK - Campo estado")
        pyautogui.click(250, 300)
        time.sleep(1)
        
        pyautogui.write("ap352")    # Digitar código do estado SP
        time.sleep(0.5)
        pyautogui.press('enter')
        time.sleep(0.5)

        print("🖱️ QUINTO CLICK - Selecionar dia atual")
        pyautogui.click(580, 323)
        time.sleep(0.5)

        print("🖱️ sexto CLICK - go")
        pyautogui.click(408, 346)
        time.sleep(3)

        print("🖱️ décimo CLICK - Selecionar planilha")
        pyautogui.click(150, 425)
        time.sleep(0.5)

        print("🖱️ décimo primeiro CLICK - Editar planilha")
        pyautogui.click(169, 450)
        time.sleep(4.5)

        print("🖱️ Clicando no campo de valor...")
        pyautogui.click(370, 478)  # 📍 Coordenada do campo valor
        time.sleep(1)
        pyautogui.hotkey('ctrl', 'a')  # Selecionar tudo  
        valor_formatado = f"{dados_planilha['valor_total']:,.2f}".replace('.', 'X').replace(',', '.').replace('X', ',')
        pyautogui.write(str(valor_formatado))
        time.sleep(1)

        print("🖱️ Clicando no campo de comentario...")
        pyautogui.click(300, 620)  # 📍 Coordenada do campo valor
        time.sleep(1)
        pyautogui.hotkey('ctrl', 'a')  # Selecionar tudo
        pyautogui.write(str(dados_planilha['comentario']))
        time.sleep(1)
        print("🖱️ Clicando no campo de invoice comment...")
        pyautogui.click(800, 620)  # 📍 Coordenada do campo valor
        time.sleep(1)
        pyautogui.hotkey('ctrl', 'a')  # Selecionar tudo
        pyautogui.write(str(dados_planilha['comentario']))
        time.sleep(1)
        print("🖱️ Clicando no upload de planilha")
        pyautogui.click(420, 665)  # 📍 Coordenada do campo valor
        time.sleep(1.5)
        pyautogui.press('f4')
        time.sleep(1)
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.5)
        print("🖱️ Obtendo caminho da planilha")
        pyautogui.write(os.path.dirname(obter_caminho_planilha(dados_planilha['tipo'])))
        time.sleep(0.5)
        pyautogui.press('enter')
        pyautogui.press('enter')
        time.sleep(15)  # Espera a janela abrir
        pyautogui.press('f6')
        time.sleep(0.2)
        pyautogui.press('f6')
        time.sleep(0.2)
        pyautogui.press('f6')
        time.sleep(0.2)
        pyautogui.press('f6')
        time.sleep(0.2)
        pyautogui.press('f6')
        time.sleep(0.2)
        pyautogui.write(str(os.path.basename(obter_caminho_planilha(dados_planilha['tipo']))))
        time.sleep(0.5)
        pyautogui.press('enter')    
        time.sleep(3) 
        print("🖱️ Clicando no update de planilha")
        pyautogui.click(190, 695)  # 📍 Coordenada do campo valor
        time.sleep(1.5)
        observacao = "Update de planilha, Price e Nº de candidatos."
        pyautogui.write(str(observacao))
        pyautogui.press('enter')
        time.sleep(1)
        pyautogui.write(str(observacao))
        pyautogui.press('enter')
        time.sleep(7)  # Espera o upload completar 
        print("✅ Navegação concluída!")
        input("\nPressione Enter para continuar...")
        return True
        
    except Exception as e:
        print(f"❌ Erro na navegação: {e}")
        return False

def selecionar_tipo_planilha(tipo_planilha):
    """Seleciona o tipo de planilha baseado na escolha"""
    print(f"📋 SELECIONANDO TIPO: {tipo_planilha}...")
    
    try:
        # 4º clique - Campo de seleção do tipo de planilha
        # (Você vai precisar descobrir essa coordenada)
        pyautogui.click(280, 240)   # 👈 AJUSTE ESTA COORDENADA!
        time.sleep(1)
        
        # Digitar o código correspondente ao tipo
        if tipo_planilha == "VUE":
            pyautogui.write("vue")    # Código para VUE
        elif tipo_planilha == "Kryterion":
            pyautogui.write("kryterion")    # Código para Kryterion
        elif tipo_planilha == "PSI":
            pyautogui.write("psi")    # Código para PSI

        time.sleep(0.5)
        pyautogui.click(410, 345) # confirmar botão GO
        time.sleep(2)

        pyautogui.click(150, 425) # seleciona a planilha
        time.sleep(0.5)

        pyautogui.click(160, 450) # visualizar planilha
        time.sleep(0.5)

        print(f"✅ Tipo {tipo_planilha} selecionado!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao selecionar tipo: {e}")
        return False
