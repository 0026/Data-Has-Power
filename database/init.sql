CREATE DATABASE IF NOT EXISTS mydb;

USE mydb;

CREATE TABLE survive_rate_by_class_and_sex(
	Sex varchar(255),
	Pclass int,
	survival_rate double
);

CREATE TABLE survive_rate_by_age_and_sex(
	Sex varchar(255),
	age_interval varchar(255),
	survival_rate double
);

CREATE TABLE survive_rate_by_age(
	age_interval varchar(255),
	survival_rate double
);
