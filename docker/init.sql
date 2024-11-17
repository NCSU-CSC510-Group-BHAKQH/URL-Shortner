CREATE DATABASE IF NOT EXISTS urlshortner;

CREATE USER IF NOT EXISTS 'root'@'localhost' IDENTIFIED BY 'admin123';

GRANT ALL PRIVILEGES ON urlshortner.* TO 'root'@'localhost';

FLUSH PRIVILEGES;
