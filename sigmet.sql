# Host: localhost  (Version 5.5.5-10.4.28-MariaDB)
# Date: 2023-06-12 02:24:34
# Generator: MySQL-Front 6.0  (Build 2.20)


#
# Structure for table "extracted_sigmet"
#

DROP TABLE IF EXISTS `extracted_sigmet`;
CREATE TABLE `extracted_sigmet` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `release_date` date DEFAULT NULL,
  `release_time` time DEFAULT NULL,
  `sigmet` text NOT NULL,
  `status` varchar(10) DEFAULT NULL,
  `sigmet_code` char(2) DEFAULT NULL,
  `cancelation_sigmet_code` varchar(2) DEFAULT NULL,
  `valid_date` varchar(30) DEFAULT NULL,
  `flight_information` varchar(15) DEFAULT NULL,
  `mountain` varchar(10) DEFAULT NULL,
  `mountain_pos` varchar(60) DEFAULT NULL,
  `observed_at` varchar(5) DEFAULT NULL,
  `polygon` varchar(255) DEFAULT NULL,
  `flight_level` varchar(4) DEFAULT NULL,
  `va_movement` varchar(7) DEFAULT NULL,
  `va_speed` varchar(12) DEFAULT NULL,
  `intensitivity` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

#
# Data for table "extracted_sigmet"
#

