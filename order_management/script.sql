/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 80040 (8.0.40)
 Source Host           : localhost:3306
 Source Schema         : db_order_0823

 Target Server Type    : MySQL
 Target Server Version : 80040 (8.0.40)
 File Encoding         : 65001

 Date: 01/09/2025 17:02:31
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for t_cart
-- ----------------------------
DROP TABLE IF EXISTS `t_cart`;
CREATE TABLE `t_cart`  (
  `food_id` int NOT NULL,
  `user_id` int NOT NULL,
  `amount` decimal(8, 2) NOT NULL DEFAULT 0.00,
  `subtotal` decimal(8, 2) NOT NULL DEFAULT 0.00,
  PRIMARY KEY (`food_id`, `user_id`) USING BTREE,
  INDEX `food_id`(`food_id` ASC) USING BTREE,
  INDEX `user_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `t_cart_ibfk_1` FOREIGN KEY (`food_id`) REFERENCES `t_food` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `t_cart_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `t_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of t_cart
-- ----------------------------

-- ----------------------------
-- Table structure for t_food
-- ----------------------------
DROP TABLE IF EXISTS `t_food`;
CREATE TABLE `t_food`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `price` decimal(8, 2) NOT NULL,
  `specs` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `status` int NOT NULL DEFAULT 1,
  `create_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `idx_food_name`(`name` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of t_food
-- ----------------------------
INSERT INTO `t_food` VALUES (1, '青椒炒肉', 15.00, '份', 1, '2025-08-23 15:01:20', '2025-08-23 15:01:20');
INSERT INTO `t_food` VALUES (2, '香辣鱼片', 23.00, '份', 1, '2025-08-23 15:01:20', '2025-08-28 15:04:14');
INSERT INTO `t_food` VALUES (3, '红焖羊肉', 19.00, '碗', 1, '2025-08-23 15:01:20', '2025-08-28 15:05:54');
INSERT INTO `t_food` VALUES (5, '黑椒牛排', 43.00, '份', 1, '2025-08-28 20:45:38', '2025-08-28 20:45:38');

-- ----------------------------
-- Table structure for t_order
-- ----------------------------
DROP TABLE IF EXISTS `t_order`;
CREATE TABLE `t_order`  (
  `order_no` char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `user_id` int NOT NULL,
  `order_person` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `order_phone` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `order_address` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `sum_price` decimal(8, 2) NULL DEFAULT 0.00,
  `status` int NULL DEFAULT 0,
  `create_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `update_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`order_no`) USING BTREE,
  INDEX `idx_order_user`(`user_id` ASC) USING BTREE,
  CONSTRAINT `t_order_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `t_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of t_order
-- ----------------------------
INSERT INTO `t_order` VALUES ('7f5890d3d6', 3, '王五', '15012324911', '北京', 38.00, 6, '2025-09-01 16:54:04', '2025-09-01 17:00:12');

-- ----------------------------
-- Table structure for t_order_details
-- ----------------------------
DROP TABLE IF EXISTS `t_order_details`;
CREATE TABLE `t_order_details`  (
  `order_no` char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `food_id` int NOT NULL,
  `amount` decimal(8, 2) NOT NULL,
  `subtotal` decimal(8, 2) NOT NULL,
  PRIMARY KEY (`order_no`, `food_id`) USING BTREE,
  INDEX `idx_orderdetail_food`(`food_id` ASC) USING BTREE,
  CONSTRAINT `t_order_details_ibfk_1` FOREIGN KEY (`order_no`) REFERENCES `t_order` (`order_no`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `t_order_details_ibfk_2` FOREIGN KEY (`food_id`) REFERENCES `t_food` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of t_order_details
-- ----------------------------
INSERT INTO `t_order_details` VALUES ('7f5890d3d6', 1, 1.00, 15.00);
INSERT INTO `t_order_details` VALUES ('7f5890d3d6', 2, 1.00, 23.00);

-- ----------------------------
-- Table structure for t_refund_application
-- ----------------------------
DROP TABLE IF EXISTS `t_refund_application`;
CREATE TABLE `t_refund_application`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `order_no` char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `user_id` int NOT NULL,
  `refund_reason` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `refund_response` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `refund_amount` decimal(8, 2) NOT NULL,
  `status` int NOT NULL,
  `create_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_refund_user`(`user_id` ASC) USING BTREE,
  INDEX `idx_refund_order`(`order_no` ASC) USING BTREE,
  CONSTRAINT `t_refund_application_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `t_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `t_refund_application_ibfk_2` FOREIGN KEY (`order_no`) REFERENCES `t_order` (`order_no`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of t_refund_application
-- ----------------------------
INSERT INTO `t_refund_application` VALUES (5, '7f5890d3d6', 3, '就不想要了？', '滚蛋', 38.00, 2, '2025-09-01 16:54:43', '2025-09-01 16:56:23');
INSERT INTO `t_refund_application` VALUES (6, '7f5890d3d6', 3, '给你8块，求你退我。', '好吧，给你通过了', 30.00, 1, '2025-09-01 16:59:18', '2025-09-01 17:00:12');

-- ----------------------------
-- Table structure for t_user
-- ----------------------------
DROP TABLE IF EXISTS `t_user`;
CREATE TABLE `t_user`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `password` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `balance` decimal(8, 2) NOT NULL DEFAULT 0.00,
  `status` int NOT NULL DEFAULT 1,
  `role` int NOT NULL DEFAULT 1,
  `create_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `idx_user_username`(`username` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of t_user
-- ----------------------------
INSERT INTO `t_user` VALUES (1, 'admin', '123456', 5000.00, 1, 0, '2025-08-23 15:01:20', '2025-08-23 15:01:20');
INSERT INTO `t_user` VALUES (2, 'xiao', '286300', 1100.00, 1, 1, '2025-08-23 15:01:20', '2025-08-28 14:28:01');
INSERT INTO `t_user` VALUES (3, 'wang', '123456', 754.00, 1, 1, '2025-08-28 15:37:55', '2025-09-01 17:00:12');
INSERT INTO `t_user` VALUES (4, 'zhao', '123123', 4.50, 1, 1, '2025-08-28 21:13:19', '2025-08-30 22:05:12');

SET FOREIGN_KEY_CHECKS = 1;
