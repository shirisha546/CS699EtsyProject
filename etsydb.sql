-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 24, 2024 at 06:49 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `etsydb`
--

-- --------------------------------------------------------

--
-- Table structure for table `admins`
--

CREATE TABLE `admins` (
  `admin_id` int(11) NOT NULL,
  `firstname` varchar(50) DEFAULT NULL,
  `lastname` varchar(50) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admins`
--

INSERT INTO `admins` (`admin_id`, `firstname`, `lastname`, `email`, `password`) VALUES
(1, 'Shirisha ', 'JagdAdmin', 'shirisha@gmail.com', '$2b$12$Ymyw/OaWne/bYZpGDVlCmOgjkD3t.2aGx1FT25j0KAeWFrfB.FugS');

-- --------------------------------------------------------

--
-- Table structure for table `customers`
--

CREATE TABLE `customers` (
  `id` int(11) NOT NULL,
  `firstname` varchar(100) NOT NULL,
  `lastname` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `customers`
--

INSERT INTO `customers` (`id`, `firstname`, `lastname`, `email`, `password`) VALUES
(3, 'Shirisha', 'Jagd', 'shirisha@gmail.com', '$2b$12$Ymyw/OaWne/bYZpGDVlCmOgjkD3t.2aGx1FT25j0KAeWFrfB.FugS'),
(4, 'Shirisha', 'Second', 'shirishas@gmail.com', '$2b$12$31d7FwZ5wHaOFEHTV5cp0eamlBa7LdKjUbbQK6KRzP2U8Vrc7z/RG');

-- --------------------------------------------------------

--
-- Table structure for table `loyaltypoints`
--

CREATE TABLE `loyaltypoints` (
  `id` int(11) NOT NULL,
  `customerid` int(11) DEFAULT NULL,
  `points_earned` int(11) DEFAULT NULL,
  `date_earned` datetime DEFAULT NULL,
  `status` varchar(255) NOT NULL DEFAULT 'active',
  `display_status` varchar(255) NOT NULL DEFAULT 'new'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `loyaltypoints`
--

INSERT INTO `loyaltypoints` (`id`, `customerid`, `points_earned`, `date_earned`, `status`, `display_status`) VALUES
(1, 3, 10, '2024-04-23 14:20:37', 'active', 'new'),
(2, 3, 10, '2024-04-23 14:58:38', 'redeemed', 'new'),
(3, 3, 10, '2024-04-23 15:59:48', 'active', 'new'),
(4, 3, 10, '2024-04-23 17:36:21', 'active', 'new');

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE `products` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `name` varchar(255) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `description` text DEFAULT NULL,
  `category` varchar(255) DEFAULT NULL,
  `image_path` varchar(255) DEFAULT NULL,
  `type` varchar(255) NOT NULL DEFAULT 'sales'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`id`, `name`, `price`, `description`, `category`, `image_path`, `type`) VALUES
(11, 'Shirt', 1234.00, 'Testing', 'clothes', 'shirt.png', 'sales'),
(12, 'BMW Car', 200000.00, 'My good car sellign here', 'cars', 'cars.PNG', 'sales'),
(13, 'Good Shirt', 200.00, 'My good shirt is selling at 200 dollars', 'clothes', 'apparel-162192_1280.png', 'sales'),
(14, 'Table class ', 300.00, 'Table made of hard wood. classic one for your house for only 300', 'households', 'table.jpeg', 'sales'),
(15, 'Coffe Table', 150.00, 'A good coffe table for you', 'households', 'table-png-18.jpg', 'sales'),
(16, 'Samsung', 500.00, 'Samsung phone in good condition', 'electronics', 'samsung.jpeg', 'offer');

-- --------------------------------------------------------

--
-- Table structure for table `purchases`
--

CREATE TABLE `purchases` (
  `PurchaseID` int(11) NOT NULL,
  `CustomerID` int(11) DEFAULT NULL,
  `ProductID` int(11) DEFAULT NULL,
  `Quantity` int(11) DEFAULT NULL,
  `UnitPrice` decimal(10,2) DEFAULT NULL,
  `PurchaseDate` datetime DEFAULT NULL,
  `ShippingAddress` varchar(255) DEFAULT NULL,
  `PaymentMethod` varchar(50) DEFAULT NULL,
  `Status` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `purchases`
--

INSERT INTO `purchases` (`PurchaseID`, `CustomerID`, `ProductID`, `Quantity`, `UnitPrice`, `PurchaseDate`, `ShippingAddress`, `PaymentMethod`, `Status`) VALUES
(1, 3, 12, 1, 200000.00, '2024-04-23 12:22:10', '123 Oakland', 'paypal', 'paid'),
(2, 3, 13, 5, 200.00, '2024-04-23 12:22:10', '123 Oakland', 'paypal', 'paid'),
(3, 3, 11, 1, 1234.00, '2024-04-23 12:22:10', '123 Oakland', 'paypal', 'paid'),
(4, 3, 15, 5, 150.00, '2024-04-23 12:22:10', '123 Oakland', 'paypal', 'paid'),
(5, 3, 13, 3, 200.00, '2024-04-23 14:13:59', '234 BOSTON', 'credit_card', 'paid'),
(6, 3, 11, 1, 1234.00, '2024-04-23 14:13:59', '234 BOSTON', 'credit_card', 'paid'),
(7, 3, 12, 1, 200000.00, '2024-04-23 14:15:50', 'ABC TEXAS', 'credit_card', 'paid'),
(8, 3, 12, 1, 200000.00, '2024-04-23 14:17:25', 'Virgina SA 1234', 'credit_card', 'paid'),
(9, 3, 12, 1, 200000.00, '2024-04-23 14:20:37', 'boston', 'credit_card', 'paid'),
(10, 3, 12, 1, 200000.00, '2024-04-23 14:58:38', '1245 Newyork', 'cash', 'paid'),
(11, 3, 13, 1, 200.00, '2024-04-23 15:57:37', '123 street', 'cash', 'paid'),
(12, 3, 13, 1, 200.00, '2024-04-23 15:59:18', '134 final astreet', 'credit_card', 'paid'),
(13, 3, 14, 3, 300.00, '2024-04-23 15:59:48', '123 ok street', 'loyaltypoints', 'paid'),
(14, 3, 12, 1, 200000.00, '2024-04-23 17:36:21', '123 my home', 'credit_card', 'paid');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admins`
--
ALTER TABLE `admins`
  ADD PRIMARY KEY (`admin_id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `customers`
--
ALTER TABLE `customers`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `loyaltypoints`
--
ALTER TABLE `loyaltypoints`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `purchases`
--
ALTER TABLE `purchases`
  ADD PRIMARY KEY (`PurchaseID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admins`
--
ALTER TABLE `admins`
  MODIFY `admin_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `customers`
--
ALTER TABLE `customers`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `loyaltypoints`
--
ALTER TABLE `loyaltypoints`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `products`
--
ALTER TABLE `products`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT for table `purchases`
--
ALTER TABLE `purchases`
  MODIFY `PurchaseID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
