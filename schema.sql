DROP TABLE user;
DROP TABLE categories;
DROP TABLE item;
DROP TABLE bid;
DROP TABLE time;


CREATE TABLE time(
	current_time datetime DEFAULT (DATETIME(CURRENT_TIMESTAMP, 'LOCALTIME'))
	);
INSERT INTO time DEFAULT VALUES;
-- UPDATE time SET current_time=CURRENT_TIMESTAMP;



CREATE TABLE user (
	id integer PRIMARY KEY AUTOINCREMENT,
	name char(50)
);

CREATE TABLE categories(
	name varchar(20)
);

CREATE TABLE item(
	idUser integer REFERENCES user(id),
	id integer PRIMARY KEY AUTOINCREMENT, 
	categories char(50), 
	title char(50), 
	description char(255), 
	price float, 
	open int,
	end_date datetime,
	winner char(50)
);

CREATE TABLE bid(
	id int REFERENCES items(id), 
	buyer char(50), 
	price float,
	bid_time datetime
);

INSERT INTO categories VALUES 
	('Tech'), 
	('Toy'), 
	('Clothes');

--INSERT INTO user(name) VALUES 
--	('John'), 
--	('Lucy'), 
--	('Tom');

--INSERT INTO item(categories, title, description, price, open, end_date) VALUES 
--	('Tech', 'Ipad', 'Good Condition', 200.00, 1, '2016-6-18 15:00:00'), 
--	('Toy', 'Bike', 'Works well, but flat tires', 30.00, 0, '2016-3-18 16:00:00'),
--	('Clothes', 'T-Shirt', 'SIZE: medium, black and yellow, light use. MALE', 15.00, 1, '2016-3-19 15:00:00'),
--	('Toy', 'Cards', 'Swag', 10.00, 0, '2016-6-19 15:00:00');

--INSERT INTO bid(id, buyer, price, bid_time) VALUES
--	(1, 'John', 200.00, '2016-6-04 15:00:00'),
--	(2, 'Lucy', 30.00, '2016-3-04 16:00:00'),
--	(3, 'Tom', 15.00, '2016-3-05 15:00:00'),
--	(4, 'Smith', 10.00, '2016-6-05 15:00:00');

SELECT * FROM user;

SELECT * FROM categories;

SELECT * FROM item;

SELECT * FROM bid;

DROP TRIGGER IF EXISTS TimeUpdateTrigger;
CREATE TRIGGER TimeUpdateTrigger
AFTER UPDATE OF current_time ON time
	BEGIN
		UPDATE item SET open = 0 WHERE end_date <= new.current_time;
		UPDATE item SET open = 1 WHERE end_date >= new.current_time;
		UPDATE item SET winner = (SELECT buyer from bid WHERE bid.id = item.id ORDER BY bid.price DESC LIMIT 1) WHERE open = 0 AND winner IS NULL;
	END;












