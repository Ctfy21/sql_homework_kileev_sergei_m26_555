/*
    Килеев Сергей Игоревич
    Вариант №2
    Описание соревнования автогонок класса Формула-1. Включает в себя: календарь чемпионата, список автогонщиков, составы команд, результаты соревнований. Каждая запись в календаре чемпионата состоит из: названия гран-при, её номера среди других гран-при, даты проведения, страны проведения и места проведения. Каждый элемент списка автогонщиков состоит из: фамилии, имени, даты рождения, страны и количества побед гонщика. Составы команд характеризуются: названием команды, названием производителя мотора, двумя основными автогонщиками с номерами их машин, одного запасного автогонщика без номера машины, страны происхождения команды. Результаты соревнований представляют собой информацию по каждому автогонщику и каждому гран-при о месте, занятом данным автогонщиком на данном гран-при, количестве заработанных им очков на данном гран-при, времени, затраченном им на данную гонку или причине его схода, количестве кругов лидирования данного гонщика в данном гран-при.
    В одной и той же стране может проводиться несколько гран-при в один и тот же год. 
    Составы команд не могут меняться в течение года.
*/

CREATE TABLE COUNTRIES (
    id SERIAL PRIMARY KEY,
    CODE VARCHAR(3) NOT NULL UNIQUE,
    FULL_NAME VARCHAR(64) NOT NULL
); 

CREATE TABLE CHAMPIONSHIP_CALENDARS (
    id SERIAL PRIMARY KEY,
    RACE_NAME VARCHAR(64) NOT NULL,
    RACE_NUMBER INT NOT NULL CHECK (RACE_NUMBER > 0),
    RACE_SEASON_YEAR INT NOT NULL CHECK (RACE_SEASON_YEAR > 0),
    RACE_DATE TIMESTAMP NOT NULL,
    COUNTRY_LOCATION_CODE VARCHAR(3) NOT NULL REFERENCES COUNTRIES(CODE),
    COUNTRY_LOCATION_PLACE VARCHAR(64) NOT NULL,
    UNIQUE (RACE_NUMBER, RACE_SEASON_YEAR)

);

CREATE TABLE DRIVERS (
    id SERIAL PRIMARY KEY,
    GIVEN_NAME VARCHAR(64) NOT NULL,
    SURNAME VARCHAR(64) NOT NULL,
    BIRTHDAY TIMESTAMP NOT NULL,
    NATIONALITY_CODE VARCHAR(3) NOT NULL REFERENCES COUNTRIES(CODE) ON DELETE CASCADE,
    WINNINGS SMALLINT NOT NULL CHECK (WINNINGS >= 0)
);

CREATE TABLE TEAMS (
    id SERIAL PRIMARY KEY,
    TITLE VARCHAR(64) NOT NULL UNIQUE
);

CREATE TABLE TEAM_COMPOSITIONS (
    id SERIAL PRIMARY KEY,
    TEAM_ID INT NOT NULL REFERENCES TEAMS(id),
    SEASON_YEAR INT NOT NULL CHECK (SEASON_YEAR > 0),
    MOTOR_PRODUCER_NAME VARCHAR(64) NOT NULL,
    NATIONALITY_CODE VARCHAR(3) NOT NULL REFERENCES COUNTRIES(CODE),
    MAIN_DRIVER_1_ID INT NOT NULL REFERENCES DRIVERS(id),
    MAIN_DRIVER_1_NUMBER VARCHAR(16) NOT NULL,
    MAIN_DRIVER_2_ID INT NOT NULL REFERENCES DRIVERS(id),
    MAIN_DRIVER_2_NUMBER VARCHAR(16) NOT NULL,
    RESERVE_DRIVER_ID INT NOT NULL REFERENCES DRIVERS(id),
    UNIQUE (TEAM_ID, SEASON_YEAR),
    CHECK (
        MAIN_DRIVER_1_ID != MAIN_DRIVER_2_ID
        AND MAIN_DRIVER_1_ID != RESERVE_DRIVER_ID
        AND MAIN_DRIVER_2_ID != RESERVE_DRIVER_ID
    )
);

CREATE TABLE RESULTS (
    id SERIAL PRIMARY KEY,
    DRIVER_ID INT NOT NULL REFERENCES DRIVERS(id),
    GRAN_PRIX_ID INT NOT NULL REFERENCES CHAMPIONSHIP_CALENDARS(id),
    DRIVER_PLACE SMALLINT NOT NULL CHECK (DRIVER_PLACE > 0),
    DRIVER_SCORE SMALLINT NOT NULL CHECK (DRIVER_SCORE >= 0),
    DRIVER_TIME TIME,
    DRIVER_DISQUALIFIED_DESCRIPTION TEXT CHECK (
    (DRIVER_TIME IS NOT NULL AND DRIVER_DISQUALIFIED_DESCRIPTION IS NULL)
    OR
    (DRIVER_TIME IS NULL AND DRIVER_DISQUALIFIED_DESCRIPTION IS NOT NULL)),
    DRIVER_LAPS_WON SMALLINT NOT NULL CHECK (DRIVER_LAPS_WON >= 0),
    UNIQUE (DRIVER_ID, GRAN_PRIX_ID)
);


-- Осмысленные тестовые данные (по 6 записей на каждую таблицу).
-- Составы команд разнесены по сезонам: у команды 3 разных гонщика, а гонщиков всего 6.

INSERT INTO COUNTRIES (CODE, FULL_NAME) VALUES
    ('GBR', 'United Kingdom'),
    ('NLD', 'Netherlands'),
    ('MCO', 'Monaco'),
    ('ESP', 'Spain'),
    ('MEX', 'Mexico'),
    ('ITA', 'Italy');

INSERT INTO CHAMPIONSHIP_CALENDARS (
    RACE_NAME, RACE_NUMBER, RACE_SEASON_YEAR, RACE_DATE,
    COUNTRY_LOCATION_CODE, COUNTRY_LOCATION_PLACE
) VALUES
    ('Monaco Grand Prix',  1, 2024, '2024-05-26 15:00:00', 'MCO', 'Monte Carlo'),
    ('Spanish Grand Prix', 2, 2024, '2024-06-23 15:00:00', 'ESP', 'Barcelona'),
    ('British Grand Prix', 3, 2024, '2024-07-07 15:00:00', 'GBR', 'Silverstone'),
    ('Dutch Grand Prix',   4, 2024, '2024-08-25 15:00:00', 'NLD', 'Zandvoort'),
    ('Italian Grand Prix', 5, 2024, '2024-09-01 15:00:00', 'ITA', 'Monza'),
    ('Mexican Grand Prix', 6, 2024, '2024-10-27 20:00:00', 'MEX', 'Mexico City');

INSERT INTO DRIVERS (GIVEN_NAME, SURNAME, BIRTHDAY, NATIONALITY_CODE, WINNINGS) VALUES
    ('Max',     'Verstappen', '1997-09-30 00:00:00', 'NLD', 61),
    ('Lewis',   'Hamilton',   '1985-01-07 00:00:00', 'GBR', 105),
    ('Charles', 'Leclerc',    '1997-10-16 00:00:00', 'MCO', 8),
    ('Carlos',  'Sainz',      '1994-09-01 00:00:00', 'ESP', 4),
    ('Lando',   'Norris',     '1999-11-13 00:00:00', 'GBR', 4),
    ('Sergio',  'Perez',      '1990-01-26 00:00:00', 'MEX', 6);

INSERT INTO TEAMS (TITLE) VALUES
    ('Red Bull Racing'),
    ('Mercedes'),
    ('Ferrari'),
    ('McLaren'),
    ('Aston Martin'),
    ('Williams');

-- 6 составов: по 2 команды на сезон (2023–2025), гонщики 1..6 переиспользуются
INSERT INTO TEAM_COMPOSITIONS (
    TEAM_ID, SEASON_YEAR, MOTOR_PRODUCER_NAME, NATIONALITY_CODE,
    MAIN_DRIVER_1_ID, MAIN_DRIVER_1_NUMBER,
    MAIN_DRIVER_2_ID, MAIN_DRIVER_2_NUMBER,
    RESERVE_DRIVER_ID
) VALUES
    -- 2023: Red Bull + Mercedes
    (1, 2023, 'Honda RBPT', 'NLD', 1, '1',  6, '11', 5),
    (2, 2023, 'Mercedes',   'GBR', 2, '44', 5, '63', 4),
    -- 2024: Ferrari + McLaren
    (3, 2024, 'Ferrari',    'ITA', 3, '16', 4, '55', 2),
    (4, 2024, 'Mercedes',   'GBR', 5, '4',  1, '81', 6),
    -- 2025: Aston Martin + Williams
    (5, 2025, 'Mercedes',   'GBR', 2, '14', 6, '18', 3),
    (6, 2025, 'Mercedes',   'GBR', 4, '23', 5, '2',  1);

-- Результаты двух гран-при: Monaco (id=1) и Italian GP (id=5), места 1–6
INSERT INTO RESULTS (
    DRIVER_ID, GRAN_PRIX_ID, DRIVER_PLACE, DRIVER_SCORE,
    DRIVER_TIME, DRIVER_DISQUALIFIED_DESCRIPTION, DRIVER_LAPS_WON
) VALUES
    -- Monaco Grand Prix
    (1, 1, 1, 25, '02:00:32.110', NULL,              41),  -- Verstappen  — 1
    (3, 1, 2, 18, '02:00:39.854', NULL,               8),  -- Leclerc     — 2
    (5, 1, 3, 15, '02:00:45.201', NULL,               0),  -- Norris      — 3
    (2, 1, 4, 12, '02:00:52.640', NULL,               0),  -- Hamilton    — 4
    (4, 1, 5, 10, '02:01:01.118', NULL,               0),  -- Sainz       — 5
    (6, 1, 6,  8, NULL,           'Engine failure',   0),  -- Perez       — сход, 6-е
    -- Italian Grand Prix (Monza)
    (3, 5, 1, 25, '01:21:15.448', NULL,              28),  -- Leclerc     — 1
    (1, 5, 2, 18, '01:21:20.102', NULL,              19),  -- Verstappen  — 2
    (2, 5, 3, 15, '01:21:27.665', NULL,               0),  -- Hamilton    — 3
    (5, 5, 4, 12, '01:21:35.210', NULL,               0),  -- Norris      — 4
    (6, 5, 5, 10, '01:21:42.901', NULL,               0),  -- Perez       — 5
    (4, 5, 6,  8, NULL,           'Collision damage', 0);  -- Sainz       — сход, 6-е



    
