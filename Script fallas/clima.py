import os
import requests
from bs4 import BeautifulSoup
import json
import psycopg2

# 1. Obtener el contenido HTML de la página web
url = 'https://climatologia.meteochile.gob.cl/application/diario/visorEmaPrecipitacion/330020'
response = requests.get(url)
html = response.text

# 2. Analizar el HTML con BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')
print(soup)
# 3. Utilizar métodos de BeautifulSoup para extraer la información que necesitas
data = []

# Ejemplo: Obtener todos los títulos dentro de elementos <h3> con la clase 'gs-c-promo-heading__title'
titles = soup.find_all('h4')
for title in titles:
    # Obtener el texto del título
    title_text = title.text.strip()

    # Obtener el enlace asociado al título
    link = title.find('a')
    link_href = link['href'] if link else None

    # Agregar la información a la lista
    data.append({
        'title': title_text,
        'link': link_href
    })

# 4. Convertir la estructura de datos a JSON
json_data = json.dumps(data, indent=2)

# 5. Guardar el JSON en un archivo
def guardar_en_json(datos, nombre_archivo):
    # Guardar los datos en un archivo JSON
    ruta_archivo = os.path.join("Script fallas", "JSON", nombre_archivo)
    with open(ruta_archivo, 'w') as archivo:
        json.dump(datos, archivo, indent=4)

def crear_tabla_en_postgres(conexion_str, nombre_tabla, ruta_json):
    # Conectar a la base de datos
    conn = psycopg2.connect(conexion_str)
    cursor = conn.cursor()

    # Leer el archivo JSON
    with open(ruta_json, 'r') as archivo_json:
        datos_json = json.load(archivo_json)

    # Obtener todas las claves posibles de todas las instancias
    columnas = set()
    for dato in datos_json:
        columnas.update(dato.keys())

    # Crear la tabla
    crear_tabla_query = f"CREATE TABLE {nombre_tabla} ({', '.join([f'{columna} VARCHAR(255)' for columna in columnas])});"
    cursor.execute(crear_tabla_query)

    # Insertar datos en la tabla
    for dato in datos_json:
        insertar_query = f"INSERT INTO {nombre_tabla} ({', '.join(columnas)}) VALUES ({', '.join([f'%({columna})s' for columna in columnas])});"
        cursor.execute(insertar_query, dato)

    # Confirmar los cambios y cerrar la conexión
    conn.commit()
    conn.close()



# Obtener datos de la API
datos_api = json_data
print(datos_api)
if datos_api:
    # Nombre del archivo JSON de salida
    nombre_archivo_json = 'datos_clima.json'

    # Guardar los datos en el archivo JSON
    guardar_en_json(datos_api, nombre_archivo_json)

    # Configuración de la conexión a PostgreSQL
    conexion_str = "dbname=test user=test password=test host=localhost"

    # Cargar datos en PostgreSQL
    crear_tabla_en_postgres(conexion_str, "datosClima", "Script fallas/JSON/datos_clima2.json")
else:
    print("No se pudieron obtener datos de la API.")