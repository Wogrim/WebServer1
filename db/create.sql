-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema login_registration_schema
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `login_registration_schema` ;

-- -----------------------------------------------------
-- Schema login_registration_schema
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `login_registration_schema` DEFAULT CHARACTER SET utf8 ;
USE `login_registration_schema` ;

-- -----------------------------------------------------
-- Table `login_registration_schema`.`languages`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `login_registration_schema`.`languages` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `login_registration_schema`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `login_registration_schema`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(20) NULL,
  `last_name` VARCHAR(20) NULL,
  `email` VARCHAR(255) NULL,
  `password` VARCHAR(255) NULL,
  `birthdate` DATE NULL,
  `language_id` INT NOT NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE,
  INDEX `fk_users_languages_idx` (`language_id` ASC) VISIBLE,
  CONSTRAINT `fk_users_languages`
    FOREIGN KEY (`language_id`)
    REFERENCES `login_registration_schema`.`languages` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
