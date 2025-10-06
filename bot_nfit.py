from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time
import os

# Configuración del navegador (modo headless para GitHub Actions)
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("start-maximized")
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)

# Abrir la página de inicio de sesión
driver.get('https://leytonlab.nfit.app/')
print("Página cargada correctamente.")

# Ingresar el correo y la clave desde variables de entorno
correo = driver.find_element(By.XPATH, '//*[@id="email"]')
clave_input = driver.find_element(By.XPATH, '//*[@id="input-password"]')

correo.send_keys(os.getenv("NFIT_EMAIL"))
clave_input.send_keys(os.getenv("NFIT_PASS"))

# Iniciar sesión
time.sleep(2)
boton_login = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div/main/section/form/div[4]/button')))
boton_login.click()
print("Inicio de sesión exitoso.")

# Navegar hasta la sección de clases y realizar la reserva
time.sleep(2)
pedido_option = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="menu"]/nav/ul/a[3]')))
pedido_option.click()
print("Entrando a clases...")

time.sleep(2)
pedido_option = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="clases"]/div[1]/div/div[2]/button')))
pedido_option.click()

time.sleep(2)
pedido_option = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="clases"]/div[1]/div[2]/div/div[2]/div/div/div[1]')))
pedido_option.click()

time.sleep(2)
pedido_option = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="clases"]/div[1]/div[2]/div/div[2]/div/div/div/div[2]')))
pedido_option.click()

time.sleep(2)
pedido_option = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="clases"]/div[1]/div[2]/div/div[2]/div/div/div[5]')))
pedido_option.click()

time.sleep(2)
pedido_option = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="clases"]/div[1]/div[2]/div/div[3]/button[1]')))
pedido_option.click()

print("Reserva completada con éxito.")
driver.quit()
