import zipfile
import geopandas as gpd
from sqlalchemy import create_engine
import os

# Paso 1: Descomprimir el archivo KMZ para obtener el archivo KML
def extract_kml_from_kmz(kmz_file_path, output_dir):
    with zipfile.ZipFile(kmz_file_path, 'r') as kmz:
        kmz.extractall(output_dir)
        kml_filename = [name for name in kmz.namelist() if name.lower().endswith('.kml')][0]
    return os.path.join(output_dir, kml_filename)

# Paso 2: Convertir el archivo KML a GeoJSON y conservar el archivo KML original
def convert_kml_to_geojson(kml_file, geojson_file):
    # Convertir KML a GeoJSON
    command = f'ogr2ogr -f "GeoJSON" {geojson_file} {kml_file}'
    os.system(command)

# Paso 3: Parsear el archivo GeoJSON para extraer la información geoespacial
def read_geojson_to_geopandas(geojson_file):
    gdf = gpd.read_file(geojson_file)
    return gdf

# Paso 4: Conectar y almacenar en la base de datos PostGIS
def save_to_postgis(geodataframe, table_name, connection_string):
    engine = create_engine(connection_string)
    geodataframe.to_postgis(table_name, engine, if_exists='replace', index=False)

# Rutas y configuración
kmz_file_path = 'ParquesUrbanos.kmz'
output_dir = './ParquesUrbanos.kml'
table_name = 'parks'
geojson_file = 'converted.geojson'
table_name = 'parks'
connection_string = 'postgresql://test:@localhost:5432/test'

# Paso 1: Extraer el archivo KML del KMZ
kml_file_path = extract_kml_from_kmz(kmz_file_path, output_dir)

# Paso 2: Convertir el archivo KML a GeoJSON
geojson_file_path = os.path.join(output_dir, geojson_file)
convert_kml_to_geojson(kml_file_path, geojson_file_path)

# Paso 3: Leer el archivo GeoJSON y convertirlo a GeoDataFrame
gdf = read_geojson_to_geopandas(geojson_file_path)

# Paso 4: Guardar en la base de datos PostGIS
save_to_postgis(gdf, table_name, connection_string)

print(f"Datos almacenados en la tabla {table_name} de la base de datos PostGIS.")