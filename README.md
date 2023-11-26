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
```

### Añadir origen destino
```
create extension PGROUTING;
```
```
ALTER TABLE geometras_corregidas ADD COLUMN "source" integer;
ALTER TABLE geometras_corregidas ADD COLUMN "target" integer;

```

### Crear tabla geometrias

```
CREATE TABLE geometrias AS
SELECT
    ogc_fid , -- Adjust the column names based on your table schema
    camino,
    ST_LineMerge(ST_GeometryN(geom, 1)) AS geom
FROM
    geometras_corregidas;
    
select * from geometrias;
```

### Generar Network y topologia

```
SELECT pgr_nodeNetwork('geometrias', 0, 'ogc_fid', 'geom');
SELECT pgr_createTopology('geometrias_noded', 0, 'geom', 'id') AS result;
```

### Crear tabla nodo
```
CREATE TABLE node AS
 SELECT row_number() OVER (ORDER BY foo.p)::integer AS id,
 foo.p AS the_geom
 FROM (
 SELECT DISTINCT geometrias_noded.source AS p FROM geometrias_noded
 UNION
 SELECT DISTINCT geometrias_noded.target AS p FROM geometrias_noded
 ) foo
 GROUP BY foo.p;
```

### Crear tabla network
```
CREATE TABLE network AS
 SELECT a.*, b.id  as start_id, c.id as end_id
 FROM geometrias_noded AS a
 JOIN node AS b ON a.source = b.id
 JOIN node AS c ON a.target = c.id;
```

### Generar 1 ruta
```
Select cost,geom from pgr_dijkstra(
 'Select id, source, target, st_length(geom) as cost from network', 1,1540, false) as di
 JOIN network pt
 ON di.edge = pt.id ;
```

### Generar K rutas
```
Select path_id,cost,geom from pgr_KSP(
 'Select id, source, target, st_length(geom) as cost from network', 1,1540, 2, false) as di
 JOIN network pt
 ON di.edge = pt.id ;
```
