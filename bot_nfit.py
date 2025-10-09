import os
import time
import datetime
import traceback
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from telegram import Bot

# --- Cargar variables desde .env ---
load_dotenv()
EMAIL = os.getenv("NFIT_EMAIL")
PASS = os.getenv("NFIT_PASS")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

if not EMAIL or not PASS:
    raise ValueError("❌ Las credenciales NFIT no están configuradas en .env")

# --- Función para enviar mensajes a Telegram ---
def send_telegram(msg):
    if TELEGRAM_TOKEN and TELEGRAM_CHAT_ID:
        try:
            bot = Bot(TELEGRAM_TOKEN)
            bot.send_message(chat_id=int(TELEGRAM_CHAT_ID), text=msg)
        except Exception as e:
            print(f"⚠️ Error enviando mensaje a Telegram: {e}")
    print(msg)  # También imprimir en consola

# --- Configuración del navegador (modo headless) ---

options = webdriver.ChromeOptions()
options.add_argument('--headless=new')  # 👈 Usa el nuevo modo headless
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1920,1080')
options.add_argument('--start-maximized')
options.add_argument('--disable-blink-features=AutomationControlled')

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 12)

try:
    send_telegram("🔹 Iniciando bot de reserva NFIT...")

    # Abrir página de inicio de sesión
    driver.get('https://leytonlab.nfit.app/')
    send_telegram("Página cargada correctamente.")

    # Ingresar correo y clave
    correo = driver.find_element(By.XPATH,'//*[@id="email"]')
    clave_input = driver.find_element(By.XPATH,'//*[@id="input-password"]')
    correo.send_keys(EMAIL)  
    clave_input.send_keys(PASS)
    send_telegram("Credenciales ingresadas correctamente.")

    # Hacer clic en el botón de ingresar
    time.sleep(2)
    pedido_option = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '/html/body/div/div/div/main/section/form/div[4]/button')))
    pedido_option.click()
    send_telegram("Inicio de sesión realizado correctamente.")
    time.sleep(4)

    menu_clases = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="menu"]/nav/ul/a[3]')))
    menu_clases.click()
    send_telegram("Ingreso a clases correctamente.")

    time.sleep(2)
    pedido_option = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="clases"]/div[1]/div/div[2]/button')))
    pedido_option.click()
    send_telegram("Seleccionando reservas...")

    time.sleep(2)
    pedido_option = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="clases"]/div[1]/div[2]/div/div[2]/div/div/div[1]')))
    pedido_option.click()
    send_telegram("Seleccionando Crossfit...")

    time.sleep(2)

    ##

    # Obtener el día actual (en inglés en minúsculas)
    dia_semana = datetime.datetime.today().strftime('%A').lower()
    
    # Mapear días a sus XPATH
    xpath_dias = {
        'sunday':   '//*[@id="clases"]/div[1]/div[2]/div/div[2]/div/div/div/div[1]',  # Domingo
        'monday':   '//*[@id="clases"]/div[1]/div[2]/div/div[2]/div/div/div/div[2]',  # Lunes
        'tuesday':  '//*[@id="clases"]/div[1]/div[2]/div/div[2]/div/div/div/div[3]',  # Martes
        'wednesday':'//*[@id="clases"]/div[1]/div[2]/div/div[2]/div/div/div/div[4]',  # Miércoles
        'thursday': '//*[@id="clases"]/div[1]/div[2]/div/div[2]/div/div/div/div[5]',  # Jueves
        'friday': '//*[@id="clases"]/div[1]/div[2]/div/div[2]/div/div/div/div[6]',  # Viernes
        
    }
    
    # Seleccionar día
    if dia_semana in xpath_dias:
        send_telegram(f"Seleccionando día: {dia_semana.capitalize()}...")
        pedido_option = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_dias[dia_semana])))
        pedido_option.click()
    else:
        send_telegram(f"No hay opción configurada para {dia_semana}.")
        raise Exception(f"Día no configurado: {dia_semana}")
    
    # Esperar un poco antes del horario
    time.sleep(2)
    
 
    # Seleccionar horario
    if dia_semana.lower() == 'thursday':
        xpath_horario = '//*[@id="clases"]/div[1]/div[2]/div/div[2]/div/div/div[4]'
    elif dia_semana.lower() == 'friday':
        xpath_horario = '//*[@id="clases"]/div[1]/div[2]/div/div[2]/div/div/div[2]'
    else:
        xpath_horario = '//*[@id="clases"]/div[1]/div[2]/div/div[2]/div/div/div[5]'
    send_telegram("Seleccionando horario...")
    pedido_option = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_horario)))
    pedido_option.click()


    time.sleep(2)
    pedido_option = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="clases"]/div[1]/div[2]/div/div[3]/button[1]')))
    pedido_option.click()
    send_telegram("Reservando  con éxito. 🎉")

except Exception as e:
    send_telegram(f"❌ Error en NFIT Bot: {e}")
    print(traceback.format_exc())

finally:
    driver.quit()
