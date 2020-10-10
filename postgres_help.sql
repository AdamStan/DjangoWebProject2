-- creating application's user
CREATE USER app_user WITH PASSWORD = "haslo12345";
-- changing password
ALTER USER app_user WITH ENCRYPTED PASSWORD 'haslo12345';
-- creating database
CREATE DATABASE WITH OWNER = app_user;
-- removing database
DROP DATABASE IF EXISTS webportal;
-- adding permission for tests
ALTER USER app_user CREATEDB;