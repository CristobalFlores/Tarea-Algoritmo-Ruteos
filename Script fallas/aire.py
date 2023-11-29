import os
import requests
import json
import psycopg2

def obtener_datos_de_api(url):
    # Realizar la solicitud a la API
    respuesta = requests.get(url)

    # Verificar si la solicitud fue exitosa (código de respuesta 200)
    if respuesta.status_code == 200:
        # Devolver los datos en formato JSON
        return respuesta.json()
    else:
        # Imprimir un mensaje de error si la solicitud no fue exitosa
        print(f"Error al obtener datos de la API. Código de respuesta: {respuesta.status_code}")
        return None

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
url_api = 'https://api.waqi.info/feed/A76147/?token=d75a6566f3bfe512656839d1cea9cefde6184a61'

# Obtener datos de la API
datos_api = obtener_datos_de_api(url_api)

if datos_api:
    # Nombre del archivo JSON de salida
    nombre_archivo_json = 'datos_aire.json'

    # Guardar los datos en el archivo JSON
    guardar_en_json(datos_api, nombre_archivo_json)

    # Configuración de la conexión a PostgreSQL
    conexion_str = "dbname=test user=test password=test host=localhost"

    # Cargar datos en PostgreSQL
    crear_tabla_en_postgres(conexion_str,"datosAire","Script fallas/JSON/datos_aire2.json")
else:
    print("No se pudieron obtener datos de la API.")


#token = d75a6566f3bfe512656839d1cea9cefde6184a61
#por si se vence el token https://aqicn.org/data-platform/token/
#https://aqicn.org/station/chile-recoleta-maestra-lidia-torres/es/