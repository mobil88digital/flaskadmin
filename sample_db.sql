BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS `varian` (
	`id`	INTEGER,
	`varian`	TEXT,
	`description`	TEXT,
	PRIMARY KEY(`id`)
);
INSERT INTO `varian` (id,varian,description) VALUES (1,'Avanza G 1.5',NULL);
CREATE TABLE IF NOT EXISTS `user` (
	`id`	INTEGER NOT NULL,
	`first_name`	VARCHAR ( 255 ),
	`last_name`	VARCHAR ( 255 ),
	`email`	VARCHAR ( 255 ) UNIQUE,
	`password`	VARCHAR ( 255 ),
	`active`	BOOLEAN,
	`confirmed_at`	DATETIME,
	CHECK(activeIN(0,1)),
	PRIMARY KEY(`id`)
);
INSERT INTO `user` (id,first_name,last_name,email,password,active,confirmed_at) VALUES (1,'Admin',NULL,'admin','$pbkdf2-sha512$25000$2VtrrRXifO89x7h3LkVojQ$KrNFCY0HowhB6Ji/HOc4p7vHc5i5SNPmOCscepu8Emqj2hRSrWZEYjVxkpiICMxxq9JMkoAQHy9BbcM.cRHBMQ',1,NULL),
 (2,'Adh','input','adh','$pbkdf2-sha512$25000$ute6d.7dO8eY8x7j3FsLoQ$Ix3s9loqZNLi5avnSYvXS88CkrjSltVP90fVeMaqE0LgeUJXtyFik1qV7eRy61fp9xRaIZJftTgUK9MZA/2UKg',1,NULL),
 (3,'spim','admin','spim','$pbkdf2-sha512$25000$K6W0NoYwZgyh9J5zTkmJcQ$fbbe7VGEK1YsrKBNX/wsLurtcsOZZxlSdHwd5qg3lJISQMVWIQI9u8HUpWOi9t.1.5iksnGenxWJNQydmDrjhw',1,NULL),
 (4,'regional','manager','rm','$pbkdf2-sha512$25000$9r7X2lvrvbe2tlaqdc45xw$NDolBXh1h1eSdPm4kJgHvuSDLKDuvZ0ipHAVa0WWbY9yHumj6S13J.3buE/2SiusllSkUAkVHoyQ5QsHujayrw',1,NULL);
CREATE TABLE IF NOT EXISTS `transaksi` (
	`id`	INTEGER,
	`date`	TEXT,
	`year`	INTEGER,
	`transmission`	TEXT,
	`nama_stnk`	TEXT,
	`nama_penjual`	TEXT,
	`nopol`	TEXT,
	`mileage`	TEXT,
	`gtf`	INTEGER,
	`mrp`	INTEGER,
	`total`	INTEGER,
	`rekomen`	TEXT,
	`spim_id`	INTEGER,
	`rm_id`	INTEGER,
	PRIMARY KEY(`id`)
);
INSERT INTO `transaksi` (id,date,year,transmission,nama_stnk,nama_penjual,nopol,mileage,gtf,mrp,total,rekomen,spim_id,rm_id) VALUES (1,'2018-10-10 10:14:00.000000',2016,'AT','Vembry','Vembry','B1234KKK','30000',NULL,NULL,NULL,NULL,NULL,NULL),
 (2,'2018-10-10 13:27:00.000000',2016,'AT','Vembry','Vembry','B1234KKK','30000',NULL,NULL,NULL,NULL,NULL,NULL);
CREATE TABLE IF NOT EXISTS `trans_varian` (
	`trans_id`	INTEGER,
	`varian_id`	INTEGER
);
INSERT INTO `trans_varian` (trans_id,varian_id) VALUES (1,1),
 (2,1);
CREATE TABLE IF NOT EXISTS `trans_model` (
	`trans_id`	INTEGER,
	`model_id`	INTEGER
);
INSERT INTO `trans_model` (trans_id,model_id) VALUES (1,1),
 (2,2);
CREATE TABLE IF NOT EXISTS `trans_cabang` (
	`trans_id`	INTEGER,
	`cabang_id`	INTEGER
);
INSERT INTO `trans_cabang` (trans_id,cabang_id) VALUES (1,1),
 (2,1);
CREATE TABLE IF NOT EXISTS `trans_brand` (
	`trans_id`	INTEGER,
	`brand_id`	INTEGER
);
INSERT INTO `trans_brand` (trans_id,brand_id) VALUES (1,1),
 (2,2);
CREATE TABLE IF NOT EXISTS `trans_app` (
	`trans_id`	INTEGER,
	`app_id`	INTEGER
);
INSERT INTO `trans_app` (trans_id,app_id) VALUES (2,1);
CREATE TABLE IF NOT EXISTS `spim` (
	`spim_id`	INTEGER,
	`spim`	TEXT,
	PRIMARY KEY(`spim_id`)
);
INSERT INTO `spim` (spim_id,spim) VALUES (1,NULL);
CREATE TABLE IF NOT EXISTS `roles_users` (
	`user_id`	INTEGER,
	`role_id`	INTEGER,
	FOREIGN KEY(`role_id`) REFERENCES `role`(`id`),
	FOREIGN KEY(`user_id`) REFERENCES `user`(`id`)
);
INSERT INTO `roles_users` (user_id,role_id) VALUES (1,4),
 (2,1),
 (3,2),
 (4,3);
CREATE TABLE IF NOT EXISTS `role` (
	`id`	INTEGER NOT NULL,
	`name`	VARCHAR ( 80 ) UNIQUE,
	`description`	VARCHAR ( 255 ),
	PRIMARY KEY(`id`)
);
INSERT INTO `role` (id,name,description) VALUES (1,'user',NULL),
 (2,'spim',NULL),
 (3,'rm',NULL),
 (4,'superuser',NULL);
CREATE TABLE IF NOT EXISTS `rm` (
	`rm_id`	INTEGER,
	`spim_id`	INTEGER,
	`rm`	TEXT
);
INSERT INTO `rm` (rm_id,spim_id,rm) VALUES (1,NULL,NULL),
 ('',NULL,NULL);
CREATE TABLE IF NOT EXISTS `model_varian` (
	`model_id`	INTEGER,
	`varian_id`	INTEGER
);
INSERT INTO `model_varian` (model_id,varian_id) VALUES (1,1);
CREATE TABLE IF NOT EXISTS `model` (
	`id`	INTEGER,
	`model`	TEXT,
	`description`	TEXT,
	PRIMARY KEY(`id`)
);
INSERT INTO `model` (id,model,description) VALUES (1,'Avanza','toyota'),
 (2,'Terios',NULL);
CREATE TABLE IF NOT EXISTS `cabang` (
	`id`	INTEGER,
	`kode`	TEXT,
	`description`	TEXT,
	PRIMARY KEY(`id`)
);
INSERT INTO `cabang` (id,kode,description) VALUES (1,'ART','Cilandak');
CREATE TABLE IF NOT EXISTS `brand_model` (
	`brand_id`	INTEGER,
	`model_id`	INTEGER
);
INSERT INTO `brand_model` (brand_id,model_id) VALUES (1,1),
 (2,2);
CREATE TABLE IF NOT EXISTS `brand` (
	`id`	INTEGER,
	`brand`	TEXT,
	`description`	INTEGER,
	PRIMARY KEY(`id`)
);
INSERT INTO `brand` (id,brand,description) VALUES (1,'Toyota','toyota'),
 (2,'Daihatsu',NULL);
CREATE TABLE IF NOT EXISTS `appraiser` (
	`id`	INTEGER,
	`nama`	TEXT,
	PRIMARY KEY(`id`)
);
INSERT INTO `appraiser` (id,nama) VALUES (1,'Anton');
COMMIT;
