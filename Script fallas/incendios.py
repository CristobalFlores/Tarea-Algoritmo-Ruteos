import csv
import os
import requests
import json
import psycopg2
from io import StringIO  # Utilizado para convertir el CSV en una cadena

def obtener_datos_de_api(url):
    # Realizar la solicitud a la API
    respuesta = requests.get(url)

    # Verificar si la solicitud fue exitosa (código de respuesta 200)
    if respuesta.status_code == 200:
        # Devolver los datos en formato CSV
        return respuesta.text
    else:
        # Imprimir un mensaje de error si la solicitud no fue exitosa
        print(f"Error al obtener datos de la API. Código de respuesta: {respuesta.status_code}")
        return None

def csv_a_json(datos_csv):
    # Convertir datos CSV a una lista de diccionarios
    reader = csv.DictReader(StringIO(datos_csv))
    return [dict(row) for row in reader]

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

# URL de la API (reemplázala con la URL real de la API que estás utilizando)
url_api = 'https://firms.modaps.eosdis.nasa.gov/api/country/csv/e682c3a897c38dec6fe5e14618805d81/VIIRS_SNPP_NRT/CHL/1/2023-11-28'

# Obtener datos de la API en formato CSV
datos_api_csv = obtener_datos_de_api(url_api)

if datos_api_csv:
    # Convertir datos CSV a una lista de diccionarios
    datos_api_json = csv_a_json(datos_api_csv)

    # Nombre del archivo JSON de salida
    nombre_archivo_json = 'datos_incendio.json'

    # Guardar los datos en el archivo JSON
    guardar_en_json(datos_api_json, nombre_archivo_json)

    # Configuración de la conexión a PostgreSQL
    conexion_str = "dbname=test user=test password=test host=localhost"

    # Cargar datos en PostgreSQL
    crear_tabla_en_postgres(conexion_str, "Incendios", "Script fallas/JSON/datos_incendio.json")
else:
    print("No se pudieron obtener datos de la API.")



#-33.45694, -70.64827
#0,2
