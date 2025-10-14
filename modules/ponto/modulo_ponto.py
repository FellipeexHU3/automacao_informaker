import pyautogui
import time
from dotenv import load_dotenv  
import os

# Carregar variáveis do .env uma vez no início
load_dotenv() 

def bater_ponto(horario):
    """
    Executa sequência de navegação até o formulário
    e clica de acordo com o horário (entrada, almoço, volta, saída).
    """
    print("🖱️ EXECUTANDO SEQUÊNCIA DE NAVEGAÇÃO...")
    
    pyautogui.FAILSAFE = True
    
    try:
        # Pequena pausa para garantir que o usuário pode parar se algo der errado
        time.sleep(2)
        print("🖱️ PRIMEIRO CLICK - Recepção")
        pyautogui.click(22, 362)
        time.sleep(1.5)

        print("🖱️ SEGUNDO CLICK - Horários")
        pyautogui.click(23, 200)
        time.sleep(3)

        print("🖱️ TERCEIRO CLICK - Botão do horário escolhido")

        if horario == "Entrada":
            pyautogui.click(420, 375)  # exemplo de coordenada para "Entrada"
            print("✅ Marcado: ENTRADA")

        elif horario == "Almoco":
            pyautogui.click(475, 375)  # exemplo de coordenada para "Almoço"
            print("✅ Marcado: ALMOÇO")

        elif horario == "Volta":
            pyautogui.click(530, 375)  # exemplo de coordenada para "Volta do Almoço"
            print("✅ Marcado: VOLTA DO ALMOÇO")

        elif horario == "Saida":
            pyautogui.click(600, 375)  # exemplo de coordenada para "Saída"
            print("✅ Marcado: SAÍDA")

        else:
            print("❌ Horário inválido!")

        time.sleep(0.5)
        pyautogui.click(1080, 375)
        time.sleep(0.5)
        pyautogui.click(171, 420) # salvar
        print("🎉 Ponto registrado com sucesso!")

    except Exception as e:
        print(f"⚠️ Erro durante a execução: {e}")
