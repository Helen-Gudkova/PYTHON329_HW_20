SELECT *
FROM "2gis_businesses"
WHERE city = "Москва" AND email is not null
AND  (category like "кафе%" or  category like "%магазин%");