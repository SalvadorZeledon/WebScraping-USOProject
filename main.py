import subprocess

# Definir las rutas completas de los archivos que deseas ejecutar
scriptDia = "C:\\Users\\SALVADORALFREDOZELED\\desktop\\pythonProject\\xDia.py"
scriptMes = "C:\\Users\\SALVADORALFREDOZELED\\desktop\\pythonProject\\xMes.py"



# Preguntar al usuario qué archivo quiere ejecutar
print('Bienvenido! Listo para Scrapear?')
print('Haremos web scraping a WeatherCloud.net, para obtener los datos del clima, estos pueden ser los datos que se han '
      'cendado durante un dia en especifico o durante todo un mes.')
print('En base a que intervalo de tiempo deseas scrapear: ')
print('1) Scrapear base a Mes.')
print('2) Scrapear todo el Dia.')
opcion = input("opcion : ")

if opcion == "1":
    print("Ejecutando el Script 1")
    subprocess.run([r'.venv\Scripts\python', scriptMes])
elif opcion == "2":
    print("Ejecutando el Script 2")
    subprocess.run([r'.venv\Scripts\python', scriptDia])
else:
    print("Opción no válida")