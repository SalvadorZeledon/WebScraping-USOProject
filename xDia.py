from time import sleep
import bs4
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import datetime
from tqdm import tqdm
import pandas as pd
import time


#ACCEDIENDO AL REPORTE POR DIA

#Configuracion del navegador
options = webdriver.ChromeOptions()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")
options.add_argument('--start-maximized')
options.add_argument('--disable-extensions')

# Ruta de ChromeDriver
driver_path = 'C:\\Users\\SALVADORALFREDOZELED\\Desktop\\webdriver\\chromedriver-win64\\chromedriver.exe'

# Inicializar el servicio del WebDriver
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=options)
driver.maximize_window()
time.sleep(1)

#accediendo a la URL de la weathercloud
driver.get('https://app.weathercloud.net/')

#Aceptando las cookies
try:
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-primary.pull-right"))
    ).click()
    print("Aceptamos las cookies.")
except Exception as e:
    print(f"Error al aceptar las cookies: {e}")

#iniciando sesion
try:
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a.btn.btn-primary[data-toggle='modal']"))
    )
    driver.execute_script("arguments[0].click();", login_button)
    print("Se ha hecho clic en el botón de inicio de sesión.")
except Exception as e:
    print(f"Error al intentar hacer clic en el botón de inicio de sesión: {e}")

# Esperar a que el modal sea visible y luego interactuar con los campos

try:
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "input#LoginForm_entity"))
    ).send_keys('iot@usonsonate.edu.sv')
    print("Correo institucional ingresado.")
except Exception as e:
    print(f"Error al escribir el correo: {e}")

try:
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "input#LoginForm_password"))
    ).send_keys('Cuz07108!')
    print("Contraseña ingresada.")
except Exception as e:
    print(f"Error al escribir la contraseña: {e}")

# Presionar el botón de inicio de sesión
try:
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-primary.btn-large.btn-block"))
    ).click()
    print("Iniciando sesión.")
except Exception as e:
    print(f"Error al iniciar sesión: {e}")


time.sleep(2)

driver.execute_script("document.elementFromPoint(window.innerWidth - 75, 50).click();")
print('Cerramos panel de actualización.')

try:
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "i.icon-file-text"))
    ).click()
    print("cliqueamos los reportes.")
except Exception as e:
    print(f"No pudimos ingresar a los reportes: {e}")

time.sleep(2)
driver.refresh()
print('Cerramos la publicidad.')

try:
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "i.icon-file-text"))
    ).click()
    print("Clic en los reportes.")
except Exception as e:
    print(f"No pudimos ingresar a los reportes: {e}")


try:
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "span.caret"))
    ).click()
    print("Abrimos el selector de ubicación.")
except Exception as e:
    print(f"No se pudo abrir el selector de ubicación: {e}")


try:
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//span[text()='Servicio de usos múltiples' or text()='USO' or text()='uso']"))
    ).click()
    print("Seleccionamos USO.")
except Exception as e:
    print(f"No se pudo seleccionar la ubicación: {e}")

driver.execute_script("document.elementFromPoint(window.innerWidth - 75, 50).click();")
print('Cerrando el selector de ubicacion.')



try:
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//span[text()='Mes entero']"))
    ).click()
    print("Abrimos selector de fecha.")
except Exception as e:
    print(f"No se pudo seleccionar la fecha: {e}")


diActual = datetime.now().strftime('%d').lstrip('0')  # Esto te da '1', '2', etc.
print(diActual)
time.sleep(10)

# Construir el XPath dinámico usando el día actual
try:
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, f"//span[text()='{diActual}']"))
    ).click()
    print(f"Seleccionamos el día {diActual}.")
except Exception as e:
    print(f"No se pudo seleccionar la fecha: {e}")

time.sleep(1)

try:
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "a.btn.btn-primary#report-button-view"))
    ).click()
    print("Generando reporte.")
except Exception as e:
    print(f"No se pudo abrir el reporte: {e}")

time.sleep(3)

try:
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "tbody#report-modal-table-body"))
    ).click()
    print("Generando reporte.")
except Exception as e:
    print(f"No se pudo abrir el reporte: {e}")


#Accediendo al contenido de la tabla
table_html = driver.find_element(By.CSS_SELECTOR, "tbody#report-modal-table-body").get_attribute('outerHTML')

#procesando la tabla
soup = bs4.BeautifulSoup(table_html, 'lxml')
table = soup.find('tbody', {'id': 'report-modal-table-body'})

#Se inicializan las listas donde se guardaran los datos de las tablas.
fecha = []
temperatura =[]
humedad = []
presionAtmosferica = []
windSpeed = []
windSpeedMax =[]
windDirection = []
rain = []
rainIntensity = []
radiacionSolar = []
evopatranspiracion = []
indiceUV = []

# Extrayendo los datos de la tabla
for row in tqdm(table.findAll('tr')):
    cells = row.findAll('td')
    # Asegurarse de que la fila tiene suficientes celdas antes de procesarlas
    if len(cells) < 12:
        print("Fila con menos de 12 celdas encontrada, se omite.")
        continue

    #Asignando los datos
    date = cells[0].text.strip()
    temp = cells[1].text.strip()
    hum = cells[2].text.strip()
    PAtmosferica = cells[3].text.strip()
    WSpeed = cells[4].text.strip()
    WMax = cells[5].text.strip()
    WDirection = cells[6].text.strip()
    lluvia = cells[7].text.strip()
    RIntensity = cells[8].text.strip()
    RSolar = cells[9].text.strip()
    Etranspiracion = cells[10].text.strip()
    IUV = cells[11].text.strip()

    # Guardar los datos en las listas
    fecha.append(date)
    temperatura.append(temp)
    humedad.append(hum)
    presionAtmosferica.append(PAtmosferica)
    windSpeed.append(WSpeed)
    windSpeedMax.append(WMax)
    windDirection.append(WDirection)
    rain.append(lluvia)
    rainIntensity.append(RIntensity)
    radiacionSolar.append(RSolar)
    evopatranspiracion.append(Etranspiracion)
    indiceUV.append(IUV)

# Convertir los datos a un DataFrame de pandas
df = pd.DataFrame({
    'Hora': fecha,
    'Temperatura': temperatura,
    'Humedad': humedad,
    'Presion Atmosferica': presionAtmosferica,
    'Velocidad del Viento': windSpeed,
    'Velocidad Maxima del Viento': windSpeedMax,
    'Direccion del Viento': windDirection,
    'Lluvia': rain,
    'Intensidad de Lluvia': rainIntensity,
    'Radiacion Solar': radiacionSolar,
    'Evopatranspiracion': evopatranspiracion,
    'Indice UV': indiceUV
})

desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

#Inicializando los datos de la carpeta
folder_name = 'DataClima'
folder_path = os.path.join(desktop, folder_name)

#verificando si la carpeta existe, si existe no se crea pero se accede a ella
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
    print(f"Carpeta '{folder_name}' creada en el escritorio.")
else:
    print(f"Accediendo a la carpeta:  '{folder_name}'.")


# Obtener la fecha actual en formato 'YYYY-MM-DD'
current_date = datetime.now().strftime('%Y-%m-%d')

# Generar el nombre del archivo usando la fecha actual
csv_file_name = f"WeatherCloud_Report_{current_date}.csv"
csv_path = os.path.join(folder_path, csv_file_name)

# Validar si el archivo existe, de ser así, se crea un archivo nuevo con un número correlativo
file_counter = 1
while os.path.exists(csv_path):
    csv_file_name = f"WeatherCloud_Report_{current_date}_{file_counter}.csv"
    csv_path = os.path.join(folder_path, csv_file_name)
    file_counter += 1

# Guardar el DataFrame en el archivo CSV
df.to_csv(csv_path, index=False, sep=';', encoding='utf-8')

print(f"Archivo guardado en: {csv_path}")