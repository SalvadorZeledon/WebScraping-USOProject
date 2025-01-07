import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
from datetime import datetime, timedelta
import os
import bs4
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from tqdm import tqdm
import time
import numpy as np
from supabase import create_client, Client

# Configura la conexión a Supabase
url = "https://zcrzbgbmkfbclucksmtd.supabase.co"  # URL de tu proyecto Supabase
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpjcnpiZ2Jta2ZiY2x1Y2tzbXRkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzA3Nzk0NzQsImV4cCI6MjA0NjM1NTQ3NH0.lkvVSPY1UZ02yjWCKNSc0ycX4IStJpA0urHk0NhHsRE"  # Tu clave API de Supabase
supabase: Client = create_client(url, key)

def inicializar_navegador():
    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0")
    options.add_argument('--start-maximized')
    options.add_argument('--disable-extensions')

    driver_path = 'C:\\Users\\JC\\OneDrive\\Escritorio\\chromedriver-win64\\chromedriver.exe'
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    return driver

def iniciar_sesion(driver):
    driver.get('https://app.weathercloud.net/')

    # Aceptar cookies
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-primary.pull-right"))
        ).click()
        print("Aceptamos las cookies.")
    except Exception as e:
        print(f"Error al aceptar las cookies: {e}")

    # Iniciar sesión
    try:
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.btn.btn-primary[data-toggle='modal']"))
        )
        driver.execute_script("arguments[0].click();", login_button)
        print("Se ha hecho clic en el botón de inicio de sesión.")
    except Exception as e:
        print(f"Error al intentar hacer clic en el botón de inicio de sesión: {e}")

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

    # Navegar al reporte
    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "i.icon-file-text"))
        ).click()
        print("Cliqueamos los reportes.")
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

def crear_carpeta():
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    folder_name = 'DataClima'
    folder_path = os.path.join(desktop, folder_name)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Carpeta '{folder_name}' creada en el escritorio.")
    else:
        print(f"Accediendo a la carpeta: '{folder_name}'.")

    return folder_path

def realizar_scraping_diario(driver, current_date, folder_path, start_date):
    meses_espanol = ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                     "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

    fecha_actual = current_date.strftime('%Y-%m-%d')
    print(f"Scrapeando datos para la fecha: {fecha_actual}")

    # Obtener el mes y día desde current_date
    month_name = meses_espanol[current_date.month]  # Ajustamos el índice ya que va de 0 a 11
    mes_actual = meses_espanol[current_date.month]
    day = current_date.day
    print(month_name)
    print(mes_actual)
    print(day)

    time.sleep(2)
    driver.refresh()
    time.sleep(2)

    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "span.caret"))
        ).click()
        print("Abrimos el selector de ubicación.")
    except Exception as e:
        print(f"No se pudo abrir el selector de ubicación: {e}")

    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//span[text()='Servicio de usos múltiples' or text()='USO' or text()='uso']"))
        ).click()
        print("Seleccionamos USO.")
    except Exception as e:
        print(f"No se pudo seleccionar la ubicación: {e}")

    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, f"//span[text()='{mes_actual}']"))
        ).click()
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, f"//span[text()='{month_name}']"))
        ).click()
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//span[text()='Mes entero']"))
        ).click()
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, f"//span[text()='{day}']"))
        ).click()
        print(f"Fecha seleccionada: {day} de {month_name}.")
    except Exception as e:
        print(f"Error seleccionando la fecha: {e}")

    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "a.btn.btn-primary#report-button-view"))
        ).click()
        time.sleep(3)
    except Exception as e:
        print(f"No se pudo abrir el reporte: {e}")
        return

    table_html = driver.find_element(By.CSS_SELECTOR, "tbody#report-modal-table-body").get_attribute('outerHTML')
    soup = bs4.BeautifulSoup(table_html, 'lxml')
    table = soup.find('tbody', {'id': 'report-modal-table-body'})

    fecha = []
    temperatura = []
    humedad = []
    presionAtmosferica = []
    windSpeed = []
    windSpeedMax = []
    windDirection = []
    rain = []
    rainIntensity = []
    radiacionSolar = []
    evopatranspiracion = []
    indiceUV = []

    # Extrayendo los datos de la tabla
    for row in tqdm(table.findAll('tr')):
        cells = row.findAll('td')
        if len(cells) < 12:
            print("Fila con menos de 12 celdas encontrada, se omite.")
            continue

        # Asignando los datos
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

    # Crear el DataFrame para guardarlo
    df = pd.DataFrame({
        'Fecha': fecha,
        'Temperatura': temperatura,
        'Humedad': humedad,
        'Presión Atmosférica': presionAtmosferica,
        'Velocidad Viento': windSpeed,
        'Velocidad Max. Viento': windSpeedMax,
        'Dirección Viento': windDirection,
        'Lluvia': rain,
        'Intensidad de Lluvia': rainIntensity,
        'Radiación Solar': radiacionSolar,
        'Evotranspiración': evopatranspiracion,
        'Índice UV': indiceUV
    })

    fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    hora_actual = datetime.now().strftime('%H:%M:%S')  # Formato: HH:MM:SS

    # Guardar en la base de datos Supabase
    for index, row in df.iterrows():
        try:
            supabase.table('weather_data').insert({
                "fecha": fecha_actual,
                "hora": row['Fecha'],
                "temperatura": row['Temperatura'],
                "humedad": row['Humedad'],
                "presion_atmosferica": row['Presión Atmosférica'],
                "wind_speed": row['Velocidad Viento'],
                "wind_speed_max": row['Velocidad Max. Viento'],
                "wind_direction": row['Dirección Viento'],
                "rain": row['Lluvia'],
                "rain_intensity": row['Intensidad de Lluvia'],
                "radiacion_solar": row['Radiación Solar'],
                "evotranspiracion": row['Evotranspiración'],
                "indice_uv": row['Índice UV']
            }).execute()
        except Exception as e:
            print(f"Error al insertar en la base de datos: {e}")

    print("Datos insertados correctamente en Supabase.")

    # Cerrar el navegador

    def fetch_data():
        try:
            response = supabase.table('weather_data').select('*').execute()
            return response.data
        except Exception as e:
            print(f"Error al obtener los datos: {e}")
            return []

    # Guardar datos en un archivo Excel con ruta absoluta
    def save_to_excel(data):
        desktop = os.path.join(os.path.expanduser('~'), 'Desktop')

        # Inicializando los datos de la carpeta
        folder_name = 'DataClima'
        folder_path = os.path.join(desktop, folder_name)

        # Verificar si la carpeta existe; si no, se crea
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"Carpeta '{folder_name}' no existía, y ha sido creada en el escritorio.")
        else:
            print(f"Accediendo a la carpeta: '{folder_name}'.")

        # Obtener la fecha actual en formato 'YYYY-MM-DD'
        current_date = datetime.now().strftime('%Y-%m-%d')

        # Generar el nombre del archivo usando la fecha actual
        csv_file_name = f"WeatherCloud_Report_{current_date}.csv"
        csv_path = os.path.join(folder_path, csv_file_name)

        # Validar si el archivo existe; si es así, crear un archivo nuevo con un número correlativo
        file_counter = 1
        while os.path.exists(csv_path):
            csv_file_name = f"WeatherCloud_Report_{current_date}_{file_counter}.csv"
            csv_path = os.path.join(folder_path, csv_file_name)
            file_counter += 1

        df = pd.DataFrame(data)

        # Escribir los datos en un archivo CSV
        try:
            df.to_csv(csv_path, index=False, sep=';', encoding='utf-8')  # Usamos CSV para guardar
            print(f"Archivo CSV creado exitosamente en: {csv_path}")
        except Exception as e:
            print(f"Error al guardar el archivo: {e}")

    # Main
    if _name_ == '_main_':
        data = fetch_data()
        if data:
            save_to_excel(data)
        else:
            print("No hay datos para guardar.")


def star_scraping(driver, start_date, end_date):
    # Crear la carpeta para almacenar los datos
    folder_path = crear_carpeta()
    current_date = start_date

    # Bucle para iterar desde la fecha de inicio hasta la fecha final
    while current_date <= end_date:
        print(f"Scraping para la fecha: {current_date.strftime('%Y-%m-%d')}")

        # Llamar a la función realizar_scraping_diario con los argumentos correctos
        realizar_scraping_diario(driver, current_date, folder_path, start_date)

        # Avanzar al siguiente día
        current_date += timedelta(days=1)
        print(f"Avanzando al siguiente día: {current_date.strftime('%Y-%m-%d')}")

def iniciar_scraping():
    start_date = entry_start_date.get_date()  # Obtener fecha de inicio
    end_date = entry_end_date.get_date()  # Obtener fecha final
    driver = inicializar_navegador()  # Inicializar el navegador
    iniciar_sesion(driver)  # Iniciar sesión en la web
    star_scraping(driver, start_date, end_date)  # Llamar a la función de scraping
    driver.quit()  # Cerrar el navegador al finalizar el scraping

# Crear ventana principal
root = tk.Tk()
root.title("Scraping Tool")
root.geometry("400x300")
root.config(bg="#F5F5F5")

# Panel de la derecha
frame_right = tk.Frame(root, bg="#F5F5F5")
frame_right.pack(side="left", padx=20, pady=20)

# Etiquetas y entradas para las fechas
label_start = tk.Label(frame_right, text="FECHA DE INICIO", bg="#F5F5F5", font=("Arial", 10, "bold"))
label_start.pack(pady=5)
entry_start_date = DateEntry(frame_right, width=12, background="white", foreground="black", borderwidth=2)
entry_start_date.pack(pady=5)

label_end = tk.Label(frame_right, text="FECHA FINAL", bg="#F5F5F5", font=("Arial", 10, "bold"))
label_end.pack(pady=5)
entry_end_date = DateEntry(frame_right, width=12, background="white", foreground="black", borderwidth=2)
entry_end_date.pack(pady=5)

# Botón para iniciar el scraping
btn_scrape = tk.Button(frame_right, text="SCRAPEAR", bg="#D0021B", fg="white",
                       font=("Arial", 12, "bold"), width=15, command=iniciar_scraping, relief="flat")
btn_scrape.pack(pady=20)

root.mainloop()