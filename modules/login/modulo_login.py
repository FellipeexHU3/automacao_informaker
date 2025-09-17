from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os

load_dotenv()

def fazer_login():
    """Faz login no sistema e retorna o driver"""
    print("🔐 FAZENDO LOGIN...")
    
    chrome_options = Options()
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_argument('--log-level=3')
    
    servico = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=servico, options=chrome_options)
    
    try:
        driver.maximize_window()
        driver.get(os.getenv('URL_SISTEMA'))
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        ).send_keys(os.getenv('USUARIO'))
        
        driver.find_element(By.NAME, "password").send_keys(os.getenv('SENHA'))
        driver.find_element(By.ID, "btConfirmar").click()
        
        print("✅ Login realizado com sucesso!")
        return driver
        
    except Exception as e:
        print(f"❌ Erro no login: {e}")
        driver.quit()
        return None