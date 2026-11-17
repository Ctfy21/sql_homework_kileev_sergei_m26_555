-- Homework 2 --

-- Первая задача --

SELECT * FROM drivers WHERE 
    id IN(SELECT driver_id FROM results WHERE driver_place = 1 AND driver_score < 26 ORDER BY driver_laps_won DESC);

-- Вторая задача --

SELECT given_name, surname, (SELECT SUM(driver_score) FROM results WHERE results.driver_id = drivers.id) as sum_score FROM drivers ORDER BY sum_score DESC; 
 
