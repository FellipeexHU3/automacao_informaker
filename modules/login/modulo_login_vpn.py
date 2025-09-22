import pyautogui
import time
import os
from dotenv import load_dotenv


  
def fazer_login_vpn():
    load_dotenv()
    """Faz login no sistema usando automação de desktop"""
    print("🔐 FAZENDO LOGIN NA VPN...")
    
    try:
        # Abre o programa da VPN (exemplo)
        pyautogui.press('win')
        time.sleep(0.5)
        pyautogui.write('mobile VPN with SSL client')
        time.sleep(0.5)
        pyautogui.press('enter')
        time.sleep(1)
        pyautogui.press('enter')  
        time.sleep(0.5)
        pyautogui.press('tab')
        pyautogui.press('tab')
        
        # Preenche senha
        pyautogui.write(os.getenv('SENHA_VPN'))
        pyautogui.press('enter')
        
        print("✅ Login realizado com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro no login: {e}")