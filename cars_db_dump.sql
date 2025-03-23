-- MySQL dump 10.13  Distrib 8.0.39, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: Cars
-- ------------------------------------------------------
-- Server version	8.0.39

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `appointment`
--

DROP TABLE IF EXISTS `appointment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appointment` (
  `Appoint_ID` int NOT NULL AUTO_INCREMENT,
  `Date` date NOT NULL,
  `Time` time NOT NULL,
  `Purpose` varchar(255) NOT NULL,
  `Car_ID` int DEFAULT NULL,
  `Customer_ID` int DEFAULT NULL,
  PRIMARY KEY (`Appoint_ID`),
  KEY `Car_ID` (`Car_ID`),
  KEY `Customer_ID` (`Customer_ID`),
  CONSTRAINT `appointment_ibfk_1` FOREIGN KEY (`Car_ID`) REFERENCES `car` (`Car_ID`) ON DELETE CASCADE,
  CONSTRAINT `appointment_ibfk_2` FOREIGN KEY (`Customer_ID`) REFERENCES `customer` (`Customer_ID`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appointment`
--

LOCK TABLES `appointment` WRITE;
/*!40000 ALTER TABLE `appointment` DISABLE KEYS */;
INSERT INTO `appointment` VALUES (1,'2025-01-04','10:00:00','Vehicle Inspection',1,1),(2,'2025-01-05','11:30:00','Engine Check',2,2),(3,'2025-01-06','14:00:00','Tire Replacement',3,3),(5,'2025-01-29','06:01:00','Tire Replacement',2,2),(7,'2024-10-15','04:09:00','Air Bag',2,2),(8,'2025-01-24','13:25:00','Battery Replacement',2,2);
/*!40000 ALTER TABLE `appointment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `car`
--

DROP TABLE IF EXISTS `car`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `car` (
  `Car_ID` int NOT NULL AUTO_INCREMENT,
  `Model` varchar(50) NOT NULL,
  `Make` varchar(50) NOT NULL,
  `Year` int NOT NULL,
  `Price` decimal(10,2) NOT NULL,
  `Color` varchar(50) NOT NULL,
  `Status` enum('Available','Sold','Reserved','Maintenance') NOT NULL,
  `Image` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`Car_ID`),
  CONSTRAINT `car_chk_1` CHECK ((`Year` > 1900)),
  CONSTRAINT `car_chk_2` CHECK ((`Price` > 0))
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `car`
--

LOCK TABLES `car` WRITE;
/*!40000 ALTER TABLE `car` DISABLE KEYS */;
INSERT INTO `car` VALUES (1,'BMW','BMW',2021,200000.00,'Black','Sold','bmw.png'),(2,'G-Class','Mercedes',2022,150000.00,'White','Sold','Mercedes_G.png'),(3,'Range Rover','Land Rover',2020,180000.00,'White','Sold','Rang_rover.png'),(4,'BMW','BMW',2023,1800000.00,'Blue','Available','bmw.png'),(5,'Cadillac','Cadillac',2018,92000.00,'Red','Sold','Cadilac.png'),(6,'Ford','Ford',2015,40000.00,'Blue','Sold','Ford.png'),(7,'Hyundai','Hyundai',2017,30000.00,'Blue','Sold','hundai.png'),(8,'Jaguar','Jaguar',2023,1000000.00,'Black','Available','Jaguar.png'),(9,'Jeep','Jeep',2016,500000.00,'Pink','Available','Jeep.png'),(10,'KIA','KIA',2014,20000.00,'Gray','Available','KIA.png'),(11,'Mazda','Mazda',2016,200000.00,'Red','Sold','Mazda.png'),(12,'Nissan','Nissan',2021,4500000.00,'Red','Available','Nissan.png'),(13,'Opel','Opel',2020,330000.00,'Blue','Available','Opel.png'),(14,'Peugeot','Peugeot',2023,300500.00,'Blue','Sold','Peugeot.png'),(15,'Rolls Royce','Rolls Royce',2024,10000000.00,'Black','Available','Rolls_Royce.png'),(16,'Shelby','Shelby',2024,90000000.00,'Orange','Available','Shelby.png'),(17,'Skoda','Skoda',2023,900500.00,'White','Available','Skoda.png'),(18,'Tesla','Tesla',2020,65000000.00,'White','Available','Tesla.png'),(19,'Toyota Supra','Toyota',2024,50050000.00,'Yellow','Sold','toyota_super.png'),(20,'VM JEEP','VM',2022,50070000.00,'Black','Available','VM_JEEP.png'),(21,'Volkswagen','Volkswagen',2020,5003400.00,'Red','Sold','Volkswagen.png'),(22,'Volvo','Volvo',2022,990000.00,'Gray','Available','Volvo.png');
/*!40000 ALTER TABLE `car` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer`
--

DROP TABLE IF EXISTS `customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customer` (
  `Customer_ID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(100) NOT NULL,
  `Address` varchar(255) NOT NULL,
  `Phone` varchar(15) NOT NULL,
  `Email` varchar(100) NOT NULL,
  PRIMARY KEY (`Customer_ID`),
  UNIQUE KEY `Phone` (`Phone`),
  UNIQUE KEY `Email` (`Email`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer`
--

LOCK TABLES `customer` WRITE;
/*!40000 ALTER TABLE `customer` DISABLE KEYS */;
INSERT INTO `customer` VALUES (1,'Michael Brown','123 Elm Street','321-654-0987','michael.brown@example.com'),(2,'Sarah Green','456 Oak Avenue','987-123-4567','sarah.green@example.com'),(3,'Tom White','789 Maple Drive','555-678-1234','tom.white@example.com');
/*!40000 ALTER TABLE `customer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employee`
--

DROP TABLE IF EXISTS `employee`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employee` (
  `Emp_ID` int NOT NULL,
  `EmName` varchar(100) NOT NULL,
  `EmRole` varchar(50) NOT NULL,
  `Salalry` decimal(10,2) NOT NULL,
  `Statuss` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`Emp_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employee`
--

LOCK TABLES `employee` WRITE;
/*!40000 ALTER TABLE `employee` DISABLE KEYS */;
INSERT INTO `employee` VALUES (1,'John Doe','Technician',4000.00,1),(2,'Jane Smith','Salesperson',3500.00,1),(4,'Majd','Manager',2000.00,1),(6,'John Doe','Technician',50000.00,1);
/*!40000 ALTER TABLE `employee` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employee_email`
--

DROP TABLE IF EXISTS `employee_email`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employee_email` (
  `Email_ID` int NOT NULL AUTO_INCREMENT,
  `Emp_ID` int NOT NULL,
  `Email` varchar(100) NOT NULL,
  PRIMARY KEY (`Email_ID`),
  KEY `Emp_ID` (`Emp_ID`),
  CONSTRAINT `employee_email_ibfk_1` FOREIGN KEY (`Emp_ID`) REFERENCES `employee` (`Emp_ID`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employee_email`
--

LOCK TABLES `employee_email` WRITE;
/*!40000 ALTER TABLE `employee_email` DISABLE KEYS */;
INSERT INTO `employee_email` VALUES (1,1,'johndoe@example.com'),(2,2,'janesmith@example.com'),(4,4,'majd.doe@example.com');
/*!40000 ALTER TABLE `employee_email` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employee_phone`
--

DROP TABLE IF EXISTS `employee_phone`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employee_phone` (
  `Phone_ID` int NOT NULL AUTO_INCREMENT,
  `Emp_ID` int NOT NULL,
  `Phone` varchar(15) NOT NULL,
  PRIMARY KEY (`Phone_ID`),
  KEY `Emp_ID` (`Emp_ID`),
  CONSTRAINT `employee_phone_ibfk_1` FOREIGN KEY (`Emp_ID`) REFERENCES `employee` (`Emp_ID`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employee_phone`
--

LOCK TABLES `employee_phone` WRITE;
/*!40000 ALTER TABLE `employee_phone` DISABLE KEYS */;
INSERT INTO `employee_phone` VALUES (1,1,'123-456-7890'),(2,2,'987-654-3210'),(4,4,'1234567890');
/*!40000 ALTER TABLE `employee_phone` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `filter_log`
--

DROP TABLE IF EXISTS `filter_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `filter_log` (
  `Filter_ID` int NOT NULL AUTO_INCREMENT,
  `Filtered_By` varchar(255) DEFAULT NULL,
  `Year_Filter` int DEFAULT NULL,
  `Make_Filter` varchar(50) DEFAULT NULL,
  `Price_Filter` decimal(10,2) DEFAULT NULL,
  `Filter_Time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`Filter_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `filter_log`
--

LOCK TABLES `filter_log` WRITE;
/*!40000 ALTER TABLE `filter_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `filter_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_line`
--

DROP TABLE IF EXISTS `order_line`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_line` (
  `Order_Line_ID` int NOT NULL AUTO_INCREMENT,
  `Sale_ID` int NOT NULL,
  `Car_ID` int DEFAULT NULL,
  `Real_Price` decimal(20,2) NOT NULL,
  `Discount_Percentage` decimal(5,2) DEFAULT '0.00',
  `Final_Price` decimal(10,2) GENERATED ALWAYS AS ((`Real_Price` * (1 - (`Discount_Percentage` / 100)))) STORED,
  PRIMARY KEY (`Order_Line_ID`),
  KEY `Sale_ID` (`Sale_ID`),
  KEY `Car_ID` (`Car_ID`),
  CONSTRAINT `order_line_ibfk_1` FOREIGN KEY (`Sale_ID`) REFERENCES `sale` (`Sale_ID`) ON UPDATE CASCADE,
  CONSTRAINT `order_line_ibfk_2` FOREIGN KEY (`Car_ID`) REFERENCES `car` (`Car_ID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_line`
--

LOCK TABLES `order_line` WRITE;
/*!40000 ALTER TABLE `order_line` DISABLE KEYS */;
INSERT INTO `order_line` (`Order_Line_ID`, `Sale_ID`, `Car_ID`, `Real_Price`, `Discount_Percentage`) VALUES (1,1,1,200149.99,0.00),(2,2,2,150149.99,5.00),(3,3,3,25999.99,15.00),(4,4,1,200000.00,5.00),(6,2,2,10000.00,5.00),(7,7,6,40000.00,5.00),(8,8,19,50050000.00,5.00),(10,9,3,180000.00,5.00);
/*!40000 ALTER TABLE `order_line` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_line_employee`
--

DROP TABLE IF EXISTS `order_line_employee`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_line_employee` (
  `Order_Line_ID` int NOT NULL,
  `Employee_ID` int NOT NULL,
  `Role` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`Order_Line_ID`,`Employee_ID`),
  KEY `Employee_ID` (`Employee_ID`),
  CONSTRAINT `order_line_employee_ibfk_1` FOREIGN KEY (`Order_Line_ID`) REFERENCES `order_line` (`Order_Line_ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `order_line_employee_ibfk_2` FOREIGN KEY (`Employee_ID`) REFERENCES `employee` (`Emp_ID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_line_employee`
--

LOCK TABLES `order_line_employee` WRITE;
/*!40000 ALTER TABLE `order_line_employee` DISABLE KEYS */;
INSERT INTO `order_line_employee` VALUES (1,1,'Technician'),(2,2,'Salesperson');
/*!40000 ALTER TABLE `order_line_employee` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_line_service`
--

DROP TABLE IF EXISTS `order_line_service`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_line_service` (
  `Order_Line_ID` int NOT NULL,
  `Service_ID` int NOT NULL,
  PRIMARY KEY (`Order_Line_ID`,`Service_ID`),
  KEY `Service_ID` (`Service_ID`),
  CONSTRAINT `order_line_service_ibfk_1` FOREIGN KEY (`Order_Line_ID`) REFERENCES `order_line` (`Order_Line_ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `order_line_service_ibfk_2` FOREIGN KEY (`Service_ID`) REFERENCES `service` (`Service_ID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_line_service`
--

LOCK TABLES `order_line_service` WRITE;
/*!40000 ALTER TABLE `order_line_service` DISABLE KEYS */;
INSERT INTO `order_line_service` VALUES (6,1),(1,3),(2,3),(3,3);
/*!40000 ALTER TABLE `order_line_service` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `order_totals`
--

DROP TABLE IF EXISTS `order_totals`;
/*!50001 DROP VIEW IF EXISTS `order_totals`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `order_totals` AS SELECT 
 1 AS `Sale_ID`,
 1 AS `Total_Amount`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `sale`
--

DROP TABLE IF EXISTS `sale`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sale` (
  `Sale_ID` int NOT NULL AUTO_INCREMENT,
  `Date` date NOT NULL,
  `Quantity` int DEFAULT '1',
  `Customer_ID` int NOT NULL,
  `Payment_Method` enum('Visa','Cash') NOT NULL,
  `Total_Amount` decimal(10,2) NOT NULL DEFAULT '0.00',
  PRIMARY KEY (`Sale_ID`),
  KEY `Customer_ID` (`Customer_ID`),
  CONSTRAINT `sale_ibfk_1` FOREIGN KEY (`Customer_ID`) REFERENCES `customer` (`Customer_ID`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sale`
--

LOCK TABLES `sale` WRITE;
/*!40000 ALTER TABLE `sale` DISABLE KEYS */;
INSERT INTO `sale` VALUES (1,'2025-01-07',1,1,'Visa',200149.99),(2,'2025-01-08',2,2,'Cash',152142.49),(3,'2025-01-09',1,3,'Visa',22099.99),(4,'2025-01-28',1,3,'Visa',190000.00),(7,'2025-01-19',1,1,'Visa',38000.00),(8,'2025-08-07',1,1,'Visa',47547500.00),(9,'2025-01-09',1,1,'Visa',171000.00);
/*!40000 ALTER TABLE `sale` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `service`
--

DROP TABLE IF EXISTS `service`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `service` (
  `Service_ID` int NOT NULL AUTO_INCREMENT,
  `TypeSer` varchar(50) NOT NULL,
  `Date` date NOT NULL,
  `Price` decimal(10,2) NOT NULL,
  `Employee_ID` int NOT NULL,
  PRIMARY KEY (`Service_ID`),
  KEY `Employee_ID` (`Employee_ID`),
  CONSTRAINT `service_ibfk_1` FOREIGN KEY (`Employee_ID`) REFERENCES `employee` (`Emp_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `service`
--

LOCK TABLES `service` WRITE;
/*!40000 ALTER TABLE `service` DISABLE KEYS */;
INSERT INTO `service` VALUES (1,'Oil Change','2025-01-01',49.99,1),(2,'Tire Replacement','2025-01-02',99.99,2),(3,'Battery Replacement','2025-01-03',149.99,1),(4,'Oil Change','2025-02-01',50.00,1),(5,'Air Bag','2025-01-20',450.00,6);
/*!40000 ALTER TABLE `service` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'Cars'
--

--
-- Final view structure for view `order_totals`
--

/*!50001 DROP VIEW IF EXISTS `order_totals`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `order_totals` AS select `s`.`Sale_ID` AS `Sale_ID`,sum(`ol`.`Final_Price`) AS `Total_Amount` from (`sale` `s` left join `order_line` `ol` on((`s`.`Sale_ID` = `ol`.`Sale_ID`))) group by `s`.`Sale_ID` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-07-16  3:28:58
