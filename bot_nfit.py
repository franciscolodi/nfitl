import os
import time
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
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("start-maximized")
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)

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

    # Navegar a la sección de clases y reservar
    time.sleep(2)
    menu_clases = wait.until(EC.presence_of_element_located(
    (By.XPATH, '//*[@id="menu"]/nav/ul/a[3]')))
    menu_clases.click()

    time.sleep(2)
    pedido_option = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="clases"]/div[1]/div/div[2]/button')))
    pedido_option.click()
    send_telegram("Seleccionando primera clase...")

    time.sleep(2)
    pedido_option = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="clases"]/div[1]/div[2]/div/div[2]/div/div/div[1]')))
    pedido_option.click()
    send_telegram("Seleccionando horario...")

    time.sleep(2)
    pedido_option = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="clases"]/div[1]/div[2]/div/div[2]/div/div/div/div[2]')))
    pedido_option.click()
    send_telegram("Confirmando horario...")

    time.sleep(2)
    pedido_option = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="clases"]/div[1]/div[2]/div/div[2]/div/div/div[5]')))
    pedido_option.click()
    send_telegram("Seleccionando instructor...")

    time.sleep(2)
    pedido_option = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="clases"]/div[1]/div[2]/div/div[3]/button[1]')))
    pedido_option.click()
    send_telegram("Reserva completada con éxito. 🎉")

except Exception as e:
    send_telegram(f"❌ Error en NFIT Bot: {e}")
    print(traceback.format_exc())

finally:
    driver.quit()
