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
  ('A1', 0, 'iphone'),
  ('A2', 0, 'usb-c'),
  ('A3', 0, 'iphone'),
  ('A4', 0, 'usb-c'),
  ('A5', 0, 'iphone'),
  ('A6', 0, 'usb-c'),
  ('A7', 0, 'iphone'),
  ('A8', 0, 'usb-c'),
  ('B1', 0, 'usb-c'),
  ('B2', 0, 'iphone'),
  ('B3', 0, 'usb-c'),
  ('B4', 0, 'iphone'),
  ('B5', 0, 'usb-c'),
  ('B6', 0, 'iphone'),
  ('B7', 0, 'usb-c'),
  ('B8', 0, 'iphone'),
  ('C1', 0, 'iphone'),
  ('C2', 0, 'usb-c'),
  ('C3', 0, 'iphone'),
  ('C4', 0, 'usb-c'),
  ('C5', 0, 'iphone'),
  ('C6', 0, 'usb-c'),
  ('C7', 0, 'iphone'),
  ('C8', 0, 'usb-c'),
  ('D1', 0, 'usb-c'),
  ('D2', 0, 'iphone'),
  ('D3', 0, 'usb-c'),
  ('D4', 0, 'iphone'),
  ('D5', 0, 'usb-c'),
  ('D6', 0, 'iphone'),
  ('D7', 0, 'usb-c'),
  ('D8', 0, 'iphone'),
  ('E1', 0, 'iphone'),
  ('E2', 0, 'usb-c'),
  ('E3', 0, 'iphone'),
  ('E4', 0, 'usb-c'),
  ('E5', 0, 'iphone'),
  ('E6', 0, 'usb-c'),
  ('E7', 0, 'iphone'),
  ('E8', 0, 'usb-c'),
  ('F1', 0, 'micro-usb'),
  ('F2', 0, 'micro-usb'),
  ('F3', 0, 'micro-usb'),
  ('F4', 0, 'micro-usb'),
  ('F5', 0, 'micro-usb'),
  ('F6', 0, 'micro-usb'),
  ('F7', 0, 'micro-usb'),
  ('F8', 0, 'micro-usb'),
  ('P1', 0, 'parking'),
  ('P2', 0, 'parking'),
  ('P3', 0, 'parking'),
  ('P4', 0, 'parking'),
  ('P5', 0, 'parking'),
  ('P6', 0, 'parking'),
  ('P7', 0, 'parking'),
  ('P8', 0, 'parking');

