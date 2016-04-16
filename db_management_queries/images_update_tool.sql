SELECT COUNT(*) FROM images WHERE redownload_flag = 0 AND aircraft IS NOT NULL; -- out of ~112,950

--This is probably a concering group, worth more investigation
SELECT name, count(name) FROM images GROUP BY name HAVING COUNT(name) > 1

-- Find all the labels not currently used in the database
SELECT * FROM aircraft_type 
WHERE 
  aircraft_name NOT IN (SELECT DISTINCT aircraft FROM images WHERE aircraft IS NOT NULL) 
  AND aircraft_name NOT IN ('Bombardier CS100', 'Bombardier CS300', 'British Aerospace 146', 'British Aerospace Jetstream 41')
ORDER BY type_int, aircraft_name

-- Update the images 
SELECT * FROM images WHERE aircraft = 'Antonov An-148'
UPDATE images SET aircraft = 'British Aircraft Corporation One-Eleven', aircraft_type = 1 WHERE name like '%British Aircraft Corporation One-Eleven%' AND aircraft IS NULL;
UPDATE images SET aircraft = 'British Aircraft Corporation One-Eleven', aircraft_type = 1 WHERE name like '%One-Eleven%' AND aircraft IS NULL;
UPDATE images SET aircraft = 'British Aircraft Corporation One-Eleven', aircraft_type = 1 WHERE name like '%BAC One-Eleven%' AND aircraft IS NULL;
UPDATE images SET aircraft = 'British Aircraft Corporation One-Eleven', aircraft_type = 1 WHERE name like '%British Aircraft Corporation 111%' AND aircraft IS NULL;
UPDATE images SET aircraft = 'British Aircraft Corporation One-Eleven', aircraft_type = 1 WHERE name like '%BAC-111%' AND aircraft IS NULL
UPDATE images SET aircraft = 'British Aircraft Corporation One-Eleven', aircraft_type = 1 WHERE name like '%BAC 1-11%' AND aircraft IS NULL;