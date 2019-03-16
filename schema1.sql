-- MySQL dump 10.13  Distrib 5.7.22, for macos10.13 (x86_64)
--
-- Host: localhost    Database: test
-- ------------------------------------------------------
-- Server version	5.7.22

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `passbook`
--

DROP TABLE IF EXISTS `passbook`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `passbook` (
  `pid` int(11) NOT NULL AUTO_INCREMENT,
  `uid` int(11) NOT NULL,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `amount` int(11) DEFAULT NULL,
  `val` tinyint(1) DEFAULT NULL,
  `mode` varchar(20) DEFAULT NULL,
  `activity` varchar(20) DEFAULT NULL,
  `total` int(11) DEFAULT NULL,
  PRIMARY KEY (`pid`),
  KEY `FK_users` (`uid`),
  CONSTRAINT `FK_users` FOREIGN KEY (`uid`) REFERENCES `users` (`uid`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=187 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `passbook`
--

LOCK TABLES `passbook` WRITE;
/*!40000 ALTER TABLE `passbook` DISABLE KEYS */;
INSERT INTO `passbook` VALUES (22,1,'2018-08-24 13:33:00',300,1,'amazon','Updated',NULL),(40,1,'2018-08-24 19:19:34',100,0,'cash','updated',200),(42,1,'2018-08-24 19:20:43',100,0,'cash','updated',200),(59,1,'2018-08-25 14:50:26',100,1,'Person','Utkarsh',1267),(60,1,'2018-08-25 14:51:26',100,1,'Person','Utkarsh',1167),(62,1,'2018-08-25 15:05:19',15,0,'Person','Vipul',175),(88,1,'2018-08-25 17:33:10',58,1,'Cash','updated',58),(91,1,'2018-08-25 17:33:24',100,0,'Amazon','updated',-100),(98,1,'2018-08-25 18:12:00',30,0,'Cash','updated',0),(100,1,'2018-08-25 18:13:17',15,0,'Person','Vipul',0),(101,1,'2018-08-25 18:13:43',150,0,'Person','Bhupesh',15),(102,1,'2018-08-25 18:14:06',85,1,'Person','Bansal',0),(103,1,'2018-08-25 18:14:23',209,1,'Person','Debo',85),(104,1,'2018-08-25 18:14:36',15,1,'Person','Neeraj',294),(105,1,'2018-08-25 18:14:53',209,1,'Person','Preetish',309),(106,1,'2018-08-25 18:15:11',209,1,'Person','Rakshith',518),(107,1,'2018-08-25 18:15:23',209,1,'Person','Runjhun',727),(108,1,'2018-08-25 18:16:24',22,1,'Cash','Maggi',30),(109,1,'2018-08-25 18:17:13',100,1,'Person','Utkarsh',936),(110,1,'2018-08-25 18:17:50',40,1,'Person','Sattu',1036),(111,1,'2018-08-25 18:17:59',20,1,'Person','Vishal',1076),(112,1,'2018-08-25 18:18:17',245,1,'Person','Zishan',1096),(138,1,'2018-08-25 20:16:12',41,0,'Cash','updated',-11),(139,1,'2018-08-25 20:59:06',245,0,'Person','Zishan',1341),(140,1,'2018-08-25 20:59:46',245,1,'Person','Zishan',1096),(150,3,'2018-08-26 09:00:08',100,0,'Cash','updated',-100),(151,3,'2018-08-26 09:00:21',100,1,'Paytm','updated',100),(152,1,'2018-08-26 10:01:10',30,1,'Person','Vipul',1341),(162,1,'2018-08-27 06:39:53',100,0,'Person','Daksh',275),(164,1,'2018-08-27 06:40:29',20,1,'Person','Bansal',1286),(166,1,'2018-08-27 06:41:09',30,1,'Cash','Amool cool',82),(167,1,'2018-08-27 06:42:23',20,1,'Cash','E-block',52),(168,1,'2018-08-27 18:56:13',49,0,'Person','Debo',375),(169,1,'2018-08-27 18:58:58',49,1,'Cash','Maggi',81),(170,1,'2018-08-27 18:59:30',37,1,'Bank','Maaza',3541),(173,1,'2018-08-27 19:03:37',100,0,'Paytm','Updated',0),(174,1,'2018-08-27 19:04:01',52,1,'Paytm','Momos',100),(175,1,'2018-08-28 12:26:18',240,0,'Person','Vipul',375),(176,1,'2018-08-28 12:26:31',238,1,'Cash','Stuff',272),(177,1,'2018-08-28 12:28:05',205,1,'Person','Vipul',1237),(178,1,'2018-08-28 17:01:57',269,1,'Bank','Pd',3179),(179,1,'2018-08-29 10:17:53',36,1,'Paytm','Poha',48),(180,1,'2018-08-29 16:11:49',10,1,'Person','Vipul',1237),(181,1,'2018-08-29 18:47:56',30,1,'Bank','Maggi',2910),(182,1,'2018-08-29 20:30:02',70,1,'Bank','Canteen',2880),(183,1,'2018-08-30 07:52:00',122,1,'Bank','Creeze',2810),(184,1,'2018-08-30 18:00:09',1000,1,'Bank','Treat',2688),(185,1,'2018-08-30 21:09:57',45,1,'Person','Reyan',1237),(186,1,'2018-08-30 21:32:27',30,1,'Bank','Maggi',1643);
/*!40000 ALTER TABLE `passbook` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `passbook_owe`
--

DROP TABLE IF EXISTS `passbook_owe`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `passbook_owe` (
  `oid` int(11) NOT NULL AUTO_INCREMENT,
  `uid` int(11) NOT NULL,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `amount` int(11) DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`oid`),
  KEY `FK_users_o` (`uid`),
  CONSTRAINT `FK_users_o` FOREIGN KEY (`uid`) REFERENCES `users` (`uid`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `passbook_owe`
--

LOCK TABLES `passbook_owe` WRITE;
/*!40000 ALTER TABLE `passbook_owe` DISABLE KEYS */;
INSERT INTO `passbook_owe` VALUES (7,1,'2018-08-29 16:11:49',-40,'Vipul'),(8,1,'2018-08-25 18:13:43',-150,'Bhupesh'),(9,1,'2018-08-27 06:40:29',105,'Bansal'),(10,1,'2018-08-27 18:56:13',160,'Debo'),(11,1,'2018-08-26 16:02:46',0,'Neeraj'),(12,1,'2018-08-25 18:14:53',209,'Preetish'),(13,1,'2018-08-26 05:33:06',209,'Rakshith'),(14,1,'2018-08-25 18:15:23',209,'Runjhun'),(15,1,'2018-08-26 05:32:32',100,'Utkarsh'),(16,1,'2018-08-26 16:03:49',-110,'Sattu'),(17,1,'2018-08-26 16:03:29',0,'Vishal'),(18,1,'2018-08-25 20:59:46',245,'Zishan'),(20,1,'2018-08-25 21:03:21',0,'New'),(21,3,'2018-08-26 08:59:56',0,'Sid'),(22,1,'2018-08-26 14:30:39',0,'Test test'),(23,1,'2018-08-27 06:39:53',-100,'Daksh'),(24,1,'2018-08-27 06:40:37',0,'Basal'),(25,1,'2018-08-30 21:09:57',45,'Reyan');
/*!40000 ALTER TABLE `passbook_owe` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `queries`
--

DROP TABLE IF EXISTS `queries`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `queries` (
  `qid` int(11) NOT NULL AUTO_INCREMENT,
  `uid` int(11) NOT NULL,
  `username` varchar(20) NOT NULL,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `query` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`qid`),
  KEY `FK_users_q` (`uid`),
  CONSTRAINT `FK_users_q` FOREIGN KEY (`uid`) REFERENCES `users` (`uid`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `queries`
--

LOCK TABLES `queries` WRITE;
/*!40000 ALTER TABLE `queries` DISABLE KEYS */;
INSERT INTO `queries` VALUES (1,1,'sidaartha','2018-08-26 10:45:05','Test by admin');
/*!40000 ALTER TABLE `queries` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(20) DEFAULT NULL,
  `full_name` varchar(20) DEFAULT NULL,
  `sex` varchar(12) DEFAULT NULL,
  `img` mediumblob,
  `password` varchar(100) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `cash` int(11) DEFAULT NULL,
  `bank` int(11) DEFAULT NULL,
  `paytm` int(11) DEFAULT NULL,
  `amazon` int(11) DEFAULT NULL,
  `owe_in` int(11) DEFAULT NULL,
  `owe_out` int(11) DEFAULT NULL,
  PRIMARY KEY (`uid`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'sidaartha','Sidaartha Reddy','Male',NULL,'$5$rounds=535000$VMclsrxhIVsJygbC$ctpg2AkmuZ.UGdaimbx5v7lklF2TSz4R2YSNp.eQKT4','sidaarthareddy1998@gmail.com','9002981555',24,1613,12,0,1282,400),(3,'Reddy',NULL,NULL,NULL,'$5$rounds=535000$tFzkSL1YhNMNsxKP$pF/6B.xxFkEFd74GFwLgpo9b/DWEtI7fO6gzrru8PX2','reddy@gmail.com',NULL,0,0,0,0,0,0);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-08-31  3:42:20
