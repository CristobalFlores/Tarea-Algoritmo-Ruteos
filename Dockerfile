# Usa una imagen base de PostgreSQL
FROM postgis/postgis:13-master

# Establece las variables de entorno para la base de datos y el usuario
ENV POSTGRES_DB test
ENV POSTGRES_USER test
ENV POSTGRES_PASSWORD test

# Actualiza la lista de paquetes
RUN apt-get update -qq

# Instala las dependencias necesarias
RUN apt-get install -y -qq \
        postgresql-13-pgrouting \
        postgresql-13-pgrouting-scripts \
        gdal-bin

# Copia los archivos GeoPackage (gpkg) a un directorio temporal en la imagen
COPY . /tmp/


# Expone el puerto por defecto de PostgreSQL
EXPOSE 5432

# Comando por defecto al iniciar el contenedor
CMD ["postgres"]
