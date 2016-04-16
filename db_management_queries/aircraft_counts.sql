SELECT
  Aircraft,
  COUNT(*),
  SUM(use_flag = 1)
 FROM
   images
 GROUP BY
   aircraft