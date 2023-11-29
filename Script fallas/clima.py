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

def crear_tabla_en_postgres(conexion_str, datos):
    try:
        # Establecer conexión con la base de datos
        conexion = psycopg2.connect(conexion_str)
        cursor = conexion.cursor()

        # Extraer las claves del primer registro para definir las columnas
        primer_registro = datos[0]
        columnas = ", ".join(f"{key} varchar(255)" for key in primer_registro.keys())

        # Crear la nueva tabla si no existe
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS fallaClima (
                {columnas}
            )
        """)

        # Confirmar la transacción y cerrar la conexión
        conexion.commit()
        cursor.close()
        conexion.close()

        print("Tabla creada en PostgreSQL exitosamente.")
    except Exception as e:
        print(f"Error al crear la tabla en PostgreSQL: {e}")



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
    crear_tabla_en_postgres(conexion_str, datos_api)
else:
    print("No se pudieron obtener datos de la API.")