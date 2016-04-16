SELECT DISTINCT
  aircraft
FROM
  images
 WHERE
   aircraft NOT IN (SELECT aircraft_name FROM aircraft_type)