BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS `user` (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`name`	TEXT,
	`registered`	INTEGER,
	`room_id`	INTEGER NOT NULL,
	FOREIGN KEY(`room_id`) REFERENCES `room`(`id`)
);
CREATE TABLE IF NOT EXISTS `room` (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`name`	TEXT,
	`common`	INTEGER NOT NULL,
	`gpio_pin`	INTEGER NOT NULL,
	FOREIGN KEY(`gpio_pin`) REFERENCES `pin`(`pin_no`)
);
CREATE TABLE IF NOT EXISTS `pin` (
	`pin_no`	INTEGER,
	`enable`	INTEGER NOT NULL,
	PRIMARY KEY(`pin_no`)
);
CREATE TABLE IF NOT EXISTS `admin` (
	`login`	TEXT,
	`password`	TEXT,
	PRIMARY KEY(`login`)
);
COMMIT;
