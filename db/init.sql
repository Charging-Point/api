create database charging_point;
use charging_point;

CREATE TABLE locker 
    (
    id_locker VARCHAR(25), 
    locker_state INT NOT NULL,
    connector VARCHAR(25) NOT NULL,
    user_uid VARCHAR(100) DEFAULT NULL,
    deposit_time TIMESTAMP DEFAULT NULL,
     PRIMARY KEY(id_locker)
    );

CREATE TABLE charge
    (
    id_charge INT AUTO_INCREMENT, 
    id_locker VARCHAR(25) NOT NULL,
    user_uid VARCHAR(100) NOT NULL,
    deposit_time TIMESTAMP DEFAULT NULL,
    pickup_time TIMESTAMP DEFAULT NULL,	
     PRIMARY KEY(id_charge),
     FOREIGN KEY (id_locker) REFERENCES locker(id_locker)
    );


INSERT INTO locker
  (id_locker, locker_state, connector)
VALUES
  ('A1', 0, 'usb-c'),
  ('A2', 0, 'iphone'),
  ('A3', 0, 'usb-c'),
  ('A4', 0, 'iphone'),
  ('A5', 0, 'usb-c'),
  ('A6', 0, 'iphone'),
  ('A7', 0, 'usb-c'),
  ('A8', 0, 'iphone');
