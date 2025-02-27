-- prepares a MySQL server for the project

CREATE DATABASE IF NOT EXISTS onboarding;
CREATE USER IF NOT EXISTS 'onboarding_dev'@'localhost' IDENTIFIED BY 'Abanoub2910';
GRANT ALL PRIVILEGES ON `onboarding`.* TO 'onboarding_dev'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'onboarding_dev'@'localhost';
FLUSH PRIVILEGES;