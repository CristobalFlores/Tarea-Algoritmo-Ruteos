# Tarea-Algoritmo-Ruteos

### CORRER CONTENEDOR
```
docker build -t test .
```
```
docker run -d --name test -p 5432:5432 test 
```

### CONECTARSE al docker

```
docker exec -it test /bin/bash
```

### CARGAR RUTAS

```
ogr2ogr -f "PostgreSQL" PG:"dbname=test user=test password=test host=localhost port=5432" /tmp/test.gpkg
ogr2ogr -f "PostgreSQL" PG:"dbname=test user=test password=test host=localhost port=5432" /tmp/Waypoints.gpkg
ogr2ogr -f "PostgreSQL" PG:"dbname=test user=test password=test host=localhost port=5432" /tmp/muestreado.gpkg
ogr2ogr -f "PostgreSQL" PG:"dbname=test user=test password=test host=localhost port=5432" /tmp/intersecciones.gpkg
```
