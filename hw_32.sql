-- Шаг 1. Создание таблицы MarvelCharacters

CREATE TABLE MarvelCharacters (
    page_id          INTEGER,
    name             TEXT,
    urlslug          TEXT,
    identify         TEXT,
    ALIGN            TEXT,
    EYE              TEXT,
    HAIR             TEXT,
    SEX              TEXT,
    GSM              TEXT,
    ALIVE            TEXT,
    APPEARANCES      INTEGER,
    FIRST_APPEARANCE TEXT,
    Year             INTEGER
);

select * from MarvelCharacters;
---------------------------------------------------------
-- Шаг 2. Создание новой таблицы MarvelCharacters_new с первичным ключом

CREATE TABLE MarvelCharacters_new (
    id integer primary key autoincrement,
    page_id          INTEGER,
    name             TEXT,
    urlslug          TEXT,
    identify         TEXT,
    ALIGN            TEXT,
    EYE              TEXT,
    HAIR             TEXT,
    SEX              TEXT,
    GSM              TEXT,
    ALIVE            TEXT,
    APPEARANCES      INTEGER,
    FIRST_APPEARANCE TEXT,
    Year             INTEGER
);

select * from MarvelCharacters_new;
--------------------------------------------------------
-- Шаг 3. Копирование данных и удаление старой таблицы

INSERT INTO MarvelCharacters_new (page_id, name,urlslug,identify,align,eye,hair,sex,gsm,alive,APPEARANCES,FIRST_APPEARANCE,Year)
SELECT page_id, name,urlslug,identify,align,eye,hair,sex,gsm,alive,APPEARANCES,FIRST_APPEARANCE,Year FROM MarvelCharacters;

drop table MarvelCharacters;
------------------------------------------------------------
-- Шаг 4. Переименовывание новой таблицы на название старой

ALTER TABLE MarvelCharacters_new RENAME TO MarvelCharacters;
------------------------------------------------------------------------
-- Шаг 5. Создание таблиц для уникальных значений

CREATE TABLE Sex (
    sex_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE
);
select * from sex;
-------------------------------------------------------------------
CREATE TABLE EyeColor (
    eye_id INTEGER PRIMARY KEY AUTOINCREMENT,
    color TEXT UNIQUE
);

select * from EyeColor;
-------------------------------------------------------------------
CREATE TABLE HairColor (
    hair_id INTEGER PRIMARY KEY AUTOINCREMENT,
    color TEXT UNIQUE
);
select * from HairColor;
-------------------------------------------------------------------

CREATE TABLE Alignment (
    align_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE
);
select * from Alignment;
------------------------------------------------------------------

CREATE TABLE LivingStatus (
    status_id INTEGER PRIMARY KEY AUTOINCREMENT,
    status TEXT UNIQUE
);
select * from LivingStatus;
--------------------------------------------------------------------
CREATE TABLE Identity (
    identity_id INTEGER PRIMARY KEY AUTOINCREMENT,
    identity TEXT UNIQUE
);
select * from identity;
------------------------------------------------------------------
-- Шаг 6. Наполнение уникальных таблиц данными

INSERT INTO Sex (name)
SELECT DISTINCT SEX FROM MarvelCharacters;

INSERT INTO EyeColor (color)
SELECT DISTINCT EYE FROM MarvelCharacters;

INSERT INTO HairColor (color)
SELECT DISTINCT HAIR FROM MarvelCharacters;

INSERT INTO Alignment (name)
SELECT DISTINCT ALIGN FROM MarvelCharacters;

INSERT INTO LivingStatus (status)
SELECT DISTINCT  ALIVE FROM MarvelCharacters;

INSERT INTO Identity (identity)
SELECT DISTINCT IDENTIFY FROM MarvelCharacters;
-----------------------------------------------------------
-- Шаг 7. Создание Таблицы MarvelCharacters_New с Внешними Ключами

CREATE TABLE MarvelCharacters_new (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    page_id INTEGER,
    name TEXT,
    urlslug TEXT,
    identity_id INTEGER,
    align_id INTEGER,
    eye_id INTEGER,
    hair_id INTEGER,
    sex_id INTEGER,
    status_id INTEGER,
    APPEARANCES INTEGER,
    FIRST_APPEARANCE TEXT,
    Year INTEGER,
    FOREIGN KEY (identity_id) REFERENCES IDENTITY(identity_id),
    FOREIGN KEY (align_id) REFERENCES Alignment(align_id),
    FOREIGN KEY (eye_id) REFERENCES EyeColor(eye_id),
    FOREIGN KEY (hair_id) REFERENCES HairColor(hair_id),
    FOREIGN KEY (sex_id) REFERENCES Sex(sex_id),
    FOREIGN KEY (status_id) REFERENCES LivingStatus(status_id)

);
select * from MarvelCharacters_new;
----------------------------------------------------------------
-- Шаг 8. Наполнение Новой Таблицы MarvelCharacters_New с Внешними Ключами Данными

INSERT INTO MarvelCharacters_New (page_id,name,urlslug,identity_id,align_id,eye_id,hair_id,sex_id,status_id,APPEARANCES,FIRST_APPEARANCE,Year)
SELECT a.page_id, a.name,a.urlslug,
      b.identity_id, c.align_id, d.eye_id,e.hair_id,f.sex_id,g.status_id,a.APPEARANCES,a.FIRST_APPEARANCE,a.Year
FROM MarvelCharacters a
JOIN identity b ON a.identify = b.identity
JOIN Alignment c ON a.ALIGN = c.name
JOIN EyeColor d ON a.EYE = d.color
JOIN HairColor e ON a.HAIR  = e.color
JOIN Sex f ON a.SEX = f.name
JOIN LivingStatus g ON a.ALIVE = g.status
;
---------------------------------------------------------------------
-- Шаг 9-10. Удаление Старой и Переименование Новой Таблицы

drop table MarvelCharacters;

ALTER TABLE MarvelCharacters_new RENAME TO MarvelCharacters;
------------------------------------------------------------------
--Тестовые запросы--------------------------------

SELECT mc.name, s.name as Sex
   FROM MarvelCharacters mc
   JOIN Sex s ON mc.sex_id = s.sex_id;
--------------------------------------------------------------------
SELECT mc.name, ec.color as EyeColor
   FROM MarvelCharacters mc
   JOIN EyeColor ec ON mc.eye_id = ec.eye_id;
------------------------------------------------------------------
SELECT mc.name, hc.color as HairColor, ls.status as LivingStatus
   FROM MarvelCharacters mc
   JOIN HairColor hc ON mc.hair_id = hc.hair_id
   JOIN LivingStatus ls ON mc.status_id = ls.status_id;
-----------------------------------------------------------------
 SELECT mc.name, id.identity as Identity, al.name as Alignment
   FROM MarvelCharacters mc
   JOIN Identity id ON mc.identity_id = id.identity_id
   JOIN Alignment al ON mc.align_id = al.align_id;
-----------------------------------------------------------
SELECT mc.name, mc.APPEARANCES, mc.FIRST_APPEARANCE, mc.Year,
          s.name as Sex, ec.color as EyeColor, hc.color as HairColor,
          al.name as Alignment, ls.status as LivingStatus, id.identity as Identity
   FROM MarvelCharacters mc
   JOIN Sex s ON mc.sex_id = s.sex_id
   JOIN EyeColor ec ON mc.eye_id = ec.eye_id
   JOIN HairColor hc ON mc.hair_id = hc.hair_id
   JOIN Alignment al ON mc.align_id = al.align_id
   JOIN LivingStatus ls ON mc.status_id = ls.status_id
   JOIN Identity id ON mc.identity_id = id.identity_id;