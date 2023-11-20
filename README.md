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

### Añadir origen destino
```
create extension PGROUTING;
```
```
ALTER TABLE geometras_corregidas ADD COLUMN "source" integer;
ALTER TABLE geometras_corregidas ADD COLUMN "target" integer;

SELECT pgr_createTopology('geometras_corregidas', 0.001, 'geom', 'ogc_fid',clean := TRUE) AS result;

```

### Generar network

```
CREATE TABLE node AS
 SELECT row_number() OVER (ORDER BY foo.p)::integer AS id,
 foo.p AS the_geom
 FROM (
 SELECT DISTINCT geometras_corregidas.source AS p FROM geometras_corregidas
 UNION
 SELECT DISTINCT geometras_corregidas.target AS p FROM geometras_corregidas
 ) foo
 GROUP BY foo.p;
```
```

CREATE TABLE network AS
 SELECT a.*, b.id as start_id, c.id as end_id
 FROM geometras_corregidas AS a
 JOIN node AS b ON a.source = b.the_geom
 JOIN node AS c ON a.target = c.the_geom;
```
### Generar ruta

```
Select seq, node, edge,cost, geom from pgr_dijkstra(
 'Select ogc_fid as id, source, target, st_length(geom) as cost from network', 1,81, false) as di
 JOIN network pt
 ON di.edge = pt.ogc_fid ;
```

# Otra forma de cargar data

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
### Conectarse bdd y crear tabla

```
psql -U test
\c test
```
```
create extension PGROUTING;
CREATE TABLE geometras_corregidas (
    fid serial PRIMARY KEY,
    geom geometry(MultiLineString, 4326)
);
```

```
ALTER TABLE geometras_corregidas ADD COLUMN "source" integer;
ALTER TABLE geometras_corregidas ADD COLUMN "target" integer;
```

### CARGAR Data

```
ogr2ogr -f "PostgreSQL" PG:"dbname=test user=test password=test" /tmp/test.gpkg -nln geometras_corregidas -append 
```

### Generar network
```
SELECT pgr_createTopology('geometras_corregidas', 0.001, 'geom', 'fid',clean := TRUE) AS result;
```

```
CREATE TABLE node AS
 SELECT row_number() OVER (ORDER BY foo.p)::integer AS id,
 foo.p AS the_geom
 FROM (
 SELECT DISTINCT geometras_corregidas.source AS p FROM geometras_corregidas
 UNION
 SELECT DISTINCT geometras_corregidas.target AS p FROM geometras_corregidas
 ) foo
 GROUP BY foo.p;
```
```

CREATE TABLE network AS
 SELECT a.*, b.id as start_id, c.id as end_id
 FROM geometras_corregidas AS a
 JOIN node AS b ON a.source = b.the_geom
 JOIN node AS c ON a.target = c.the_geom;
```
### Generar ruta

```
Select seq, node, edge,cost, geom from pgr_dijkstra(
 'Select fid as id, source, target, st_length(geom) as cost from network', 1,81, false) as di
 JOIN network pt
 ON di.edge = pt.fid ;
```

### Generar K rutas

```
SELECT * FROM pgr_ksp(
    'SELECT fid as id, source, target, st_length(geom) as cost FROM network',
    145, 87,
    2, -- Número de caminos que deseas obtener
    false -- Valor booleano que indica si quieres obtener los caminos más cortos (true) o más largos (false)
) AS paths
JOIN network pt ON paths.edge = pt.fid;
```
