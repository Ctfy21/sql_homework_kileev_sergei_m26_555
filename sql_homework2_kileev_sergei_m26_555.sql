/*
    Килеев Сергей Игоревич
    Вариант №2
    Выберите всех гонщиков (или их идентификатор, если другой информации нет в таблице), которые заняли первое место, но заработали меньше 26 очков, отсортировав данные по убыванию кругов лидирования.
    Выберите имена и фамилии всех гонщиков и общее количество их очков, набранных по результатам гонок, и расставьте их в порядке убывания.
*/

-- Первая задача --

SELECT * FROM drivers WHERE 
    id IN(SELECT driver_id FROM results WHERE driver_place = 1 AND driver_score < 26 ORDER BY driver_laps_won DESC);

-- Вторая задача --

SELECT given_name, surname, (SELECT SUM(driver_score) FROM results WHERE results.driver_id = drivers.id) as sum_score FROM drivers ORDER BY sum_score DESC; 
 
