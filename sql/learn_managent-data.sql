/*
 Navicat Premium Data Transfer

 Source Server         : localhost_3306
 Source Server Type    : MySQL
 Source Server Version : 80200
 Source Host           : localhost:3306
 Source Schema         : learn_managent

 Target Server Type    : MySQL
 Target Server Version : 80200
 File Encoding         : 65001

 Date: 12/05/2024 10:50:00
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for assignment
-- ----------------------------
DROP TABLE IF EXISTS `assignment`;
CREATE TABLE `assignment`  (
  `id` bigint(0) NOT NULL AUTO_INCREMENT,
  `course_id` bigint(0) NULL DEFAULT NULL COMMENT '课程id',
  `assignment_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '作业名称',
  `assignment_requirement` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '作业要求',
  `submit_deadline_time` datetime(0) NULL DEFAULT NULL COMMENT '提交截至时间',
  `file_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '文件名',
  `create_time` datetime(0) NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime(0) NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP(0) COMMENT '修改时间',
  `state` tinyint(0) NULL DEFAULT 1 COMMENT '1正常 0删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '作业表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of assignment
-- ----------------------------
INSERT INTO `assignment` VALUES (1, 1, '第一章作业', '写完3道题', '2024-05-09 17:30:00', NULL, '2024-05-08 17:30:08', '2024-05-08 17:30:08', 1);
INSERT INTO `assignment` VALUES (2, 1, '第二章作业', '让人trycdsf', '2024-05-08 17:30:36', NULL, '2024-05-08 17:30:41', '2024-05-08 17:30:41', 1);
INSERT INTO `assignment` VALUES (3, 1, '第三章作业', 'dfghtj', '2024-05-17 17:31:14', NULL, '2024-05-08 17:31:18', '2024-05-08 17:31:18', 1);
INSERT INTO `assignment` VALUES (4, 3, '的氛围乳鸽汤dfgfdfge', '分为人格恒天然集团有vdfdbgnh', '2024-05-31 11:23:00', 'c91bfb65e80a4721b9bb837d262172ce.doc', '2024-05-09 09:23:59', '2024-05-09 09:26:12', 0);
INSERT INTO `assignment` VALUES (6, 1, '第四章作业', '是的哇如果让你体会有', '2024-05-26 12:00:00', 'b0bbce0ece784538888884d5e717b926.png', '2024-05-10 17:45:28', '2024-05-10 18:01:13', 0);
INSERT INTO `assignment` VALUES (7, 1, '第四章作业', '地方', '2024-05-24 11:11:00', 'e4161a81fd0848b48c22377759dc638c.png', '2024-05-10 18:01:56', '2024-05-10 21:29:16', 1);

-- ----------------------------
-- Table structure for course
-- ----------------------------
DROP TABLE IF EXISTS `course`;
CREATE TABLE `course`  (
  `id` bigint(0) NOT NULL AUTO_INCREMENT,
  `course_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '课程名称',
  `instructor_id` bigint(0) NULL DEFAULT NULL COMMENT '讲师id,对应user表id',
  `course_description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '课程描述',
  `start_date` date NULL DEFAULT NULL COMMENT '开课日期',
  `end_date` date NULL DEFAULT NULL COMMENT '结课日期',
  `create_time` datetime(0) NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime(0) NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP(0) COMMENT '修改时间',
  `state` tinyint(0) NULL DEFAULT 1 COMMENT '1正常 0删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 10 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '课程表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of course
-- ----------------------------
INSERT INTO `course` VALUES (1, '高等数学', 3, '高等数学高等数学高等数学高等数学高等数学高等数学高等数学', '2024-05-08', '2024-07-10', '2024-05-04 07:49:43', '2024-05-07 11:40:23', 1);
INSERT INTO `course` VALUES (2, '语文s', 10, '大法官提任何个人肥肉s', '2024-05-08', '2024-05-24', '2024-05-04 13:10:28', '2024-05-07 16:46:49', 1);
INSERT INTO `course` VALUES (3, '数学', 3, '的然后就谈谈个人提供', '2024-04-30', '2024-05-22', '2024-05-04 13:10:47', '2024-05-04 13:10:47', 1);
INSERT INTO `course` VALUES (4, '英语', 3, 'v复古风v发v发v发', '2024-04-29', '2024-05-30', '2024-05-04 13:11:13', '2024-05-04 13:11:13', 1);
INSERT INTO `course` VALUES (5, '体育', 3, '的非法v而发发我发', '2024-04-29', '2024-05-29', '2024-05-04 13:11:29', '2024-05-04 13:11:29', 1);
INSERT INTO `course` VALUES (6, '化学', 10, '化学', '2024-05-08', '2024-06-01', '2024-05-07 16:28:56', '2024-05-07 16:28:56', 1);
INSERT INTO `course` VALUES (7, '发表', 9, '发热刚刚认识他', '2024-05-16', '2024-06-01', '2024-05-07 16:31:07', '2024-05-07 16:35:07', 0);
INSERT INTO `course` VALUES (8, '操作系统', 3, '的得分v为', '2024-05-12', '2024-05-22', '2024-05-10 13:57:07', '2024-05-10 13:57:07', 1);
INSERT INTO `course` VALUES (9, '数据结构', 3, '参读书v', '2024-05-11', '2024-05-29', '2024-05-10 13:57:40', '2024-05-10 13:57:40', 1);
INSERT INTO `course` VALUES (10, '物理', 9, '物理物理物理物理', '2024-06-01', '2024-06-28', '2024-05-11 17:55:52', '2024-05-11 17:55:52', 1);

-- ----------------------------
-- Table structure for lecture
-- ----------------------------
DROP TABLE IF EXISTS `lecture`;
CREATE TABLE `lecture`  (
  `id` bigint(0) NOT NULL AUTO_INCREMENT,
  `instructor_id` bigint(0) NULL DEFAULT NULL COMMENT '讲师id',
  `lecture_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '讲座名称',
  `lecture_start_time` datetime(0) NULL DEFAULT NULL COMMENT '开始时间',
  `lecture_end_time` datetime(0) NULL DEFAULT NULL COMMENT '结束时间',
  `lecture_description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '讲座描述',
  `file_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '关联文件名',
  `status` tinyint(0) NULL DEFAULT 0 COMMENT '0 待审核 1已审核',
  `create_time` datetime(0) NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime(0) NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP(0) COMMENT '修改时间',
  `state` tinyint(0) NULL DEFAULT 1 COMMENT '0删除 1正常',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '讲座表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of lecture
-- ----------------------------
INSERT INTO `lecture` VALUES (1, 3, '讲座test33', '2024-05-09 19:14:00', '2024-05-09 20:14:00', '3333333333', '7aaa83fb31514220b191a46688822962.doc', 0, '2024-05-08 15:14:44', '2024-05-09 15:50:48', 0);
INSERT INTO `lecture` VALUES (2, 9, '长的跟他率', '2024-05-07 15:15:05', '2024-05-07 17:15:11', '大染缸u', '33.txt', 0, '2024-05-08 15:15:26', '2024-05-08 15:20:18', 0);
INSERT INTO `lecture` VALUES (3, 10, 'vfdbdn', '2024-05-08 15:15:38', '2024-05-08 19:15:45', 'ghjyttujyrjyt', '54364.txt', 1, '2024-05-08 15:15:59', '2024-05-08 15:16:15', 1);
INSERT INTO `lecture` VALUES (4, 3, 'fght', '2024-05-11 15:41:00', '2024-05-11 17:41:00', 'fgethryt', '7aaa83fb31514220b191a46688822962.doc', 0, '2024-05-09 15:41:59', '2024-05-09 15:41:59', 1);

-- ----------------------------
-- Table structure for message
-- ----------------------------
DROP TABLE IF EXISTS `message`;
CREATE TABLE `message`  (
  `id` bigint(0) NOT NULL AUTO_INCREMENT,
  `send_id` bigint(0) NULL DEFAULT NULL COMMENT '发送者id',
  `receive_id` bigint(0) NULL DEFAULT NULL COMMENT '接收者id',
  `message_content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '发送消息内容',
  `create_time` datetime(0) NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime(0) NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP(0) COMMENT '修改时间',
  `state` tinyint(0) NULL DEFAULT 1 COMMENT '1正常 0删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 10 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '消息表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of message
-- ----------------------------
INSERT INTO `message` VALUES (1, 2, 3, '老师你好', '2024-05-09 21:44:51', '2024-05-09 21:44:51', 1);
INSERT INTO `message` VALUES (2, 2, 3, '我的作业咋还没改', '2024-05-09 21:45:10', '2024-05-09 21:45:10', 1);
INSERT INTO `message` VALUES (3, 3, 2, '同学你好，马上改了', '2024-05-09 21:45:28', '2024-05-09 21:45:28', 1);
INSERT INTO `message` VALUES (4, 2, 3, '谢谢老师', '2024-05-09 21:45:37', '2024-05-09 21:45:37', 1);
INSERT INTO `message` VALUES (5, 3, 2, '不客气', '2024-05-09 21:45:45', '2024-05-09 21:45:45', 1);
INSERT INTO `message` VALUES (6, 3, 2, '继续加油', '2024-05-10 09:25:21', '2024-05-10 09:25:21', 1);
INSERT INTO `message` VALUES (7, 2, 3, '我会的', '2024-05-10 09:25:39', '2024-05-10 09:25:39', 1);
INSERT INTO `message` VALUES (8, 2, 3, '哈哈哈', '2024-05-11 10:17:58', '2024-05-11 10:17:58', 1);
INSERT INTO `message` VALUES (9, 2, 3, '6666', '2024-05-11 10:18:16', '2024-05-11 10:18:16', 1);
INSERT INTO `message` VALUES (10, 3, 2, '666', '2024-05-11 17:59:34', '2024-05-11 17:59:34', 1);
INSERT INTO `message` VALUES (11, 2, 3, '好好好', '2024-05-11 18:01:41', '2024-05-11 18:01:41', 1);

-- ----------------------------
-- Table structure for message_board
-- ----------------------------
DROP TABLE IF EXISTS `message_board`;
CREATE TABLE `message_board`  (
  `id` bigint(0) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(0) NULL DEFAULT NULL COMMENT '用户id',
  `message_content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '留言内容',
  `create_time` datetime(0) NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime(0) NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP(0) COMMENT '修改时间',
  `state` tinyint(0) NULL DEFAULT 1 COMMENT '1正常 0删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 9 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '公共留言区表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of message_board
-- ----------------------------
INSERT INTO `message_board` VALUES (1, 2, '今天上课听不懂啊', '2024-05-07 08:34:01', '2024-05-07 08:34:01', 1);
INSERT INTO `message_board` VALUES (2, 4, '今天三餐有鸡排饭', '2024-05-07 08:34:17', '2024-05-07 08:34:17', 1);
INSERT INTO `message_board` VALUES (3, 5, '今天下课去打篮球', '2024-05-07 08:34:34', '2024-05-07 08:34:34', 1);
INSERT INTO `message_board` VALUES (4, 6, '还不放假啊还不放假啊还不放假啊还不放假啊还不放假啊还不放假啊还不放假啊还不放假啊还不放假啊还不放假啊还不放假啊还不放假啊还不放假啊还不放假啊还不放假啊还不放假啊还不放假啊还不放假啊还不放假啊还不放假啊', '2024-05-07 08:34:48', '2024-05-10 09:57:58', 1);
INSERT INTO `message_board` VALUES (5, 8, '美羊羊咋不愿意跟我玩啊', '2024-05-07 08:35:28', '2024-05-07 08:35:28', 1);
INSERT INTO `message_board` VALUES (6, 2, '哈哈哈哈哈', '2024-05-10 10:38:25', '2024-05-10 10:51:58', 0);
INSERT INTO `message_board` VALUES (7, 2, '嘿嘿', '2024-05-10 10:52:18', '2024-05-11 18:01:15', 0);
INSERT INTO `message_board` VALUES (8, 2, 'oh no', '2024-05-10 10:54:53', '2024-05-10 10:54:56', 0);
INSERT INTO `message_board` VALUES (9, 2, '哈哈哈\n', '2024-05-11 18:01:13', '2024-05-11 18:01:13', 1);

-- ----------------------------
-- Table structure for notice
-- ----------------------------
DROP TABLE IF EXISTS `notice`;
CREATE TABLE `notice`  (
  `id` bigint(0) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(0) NULL DEFAULT NULL COMMENT '用户id',
  `notice_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '通知名称',
  `notice_content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '通知内容',
  `file_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '文件名',
  `create_time` datetime(0) NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime(0) NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP(0) COMMENT '修改时间',
  `state` tinyint(0) NULL DEFAULT 1 COMMENT '1正常 0删除',
  `type` tinyint(0) NULL DEFAULT NULL COMMENT '通知类型：1公共通知  2专属通知',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 16 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '通知表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of notice
-- ----------------------------
INSERT INTO `notice` VALUES (1, 1, '部分学生通知777', '部分学生哈哈哈哈哈7777', '300ce133a353420ead6dd65024ec7081.jpg', '2024-05-04 07:45:09', '2024-05-06 10:54:13', 1, 1);
INSERT INTO `notice` VALUES (2, 1, '部分学生通知last', '部分学生', 'a83ea3e191a740d281e5cc9e099fe08b.jpg', '2024-05-04 07:46:42', '2024-05-06 18:27:44', 1, 1);
INSERT INTO `notice` VALUES (3, 1, '哈哈哈哈哈哈', '从v非把你拖入交通银行给你回电话', 'f63a9484cbbb4d17a61f42d715455299!400x400.jpeg', '2024-05-04 07:47:00', '2024-05-05 17:12:43', 1, 1);
INSERT INTO `notice` VALUES (4, 9, '作业提醒', '的无发热沟通和肉体和', '34e1b826a7bd4a9da0816c76a8049080!400x400.jpeg', '2024-05-04 07:47:32', '2024-05-05 17:08:28', 1, 1);
INSERT INTO `notice` VALUES (5, 10, '啥感觉废话', '地方台然后又和人个人规划人太少那伙人', 'd858655ad571488fa917d57f68797088!400x400.jpeg', '2024-05-04 07:48:02', '2024-05-06 13:30:13', 0, 1);
INSERT INTO `notice` VALUES (6, 1, '全体同志', '哈韩的还是v警方公布', 'e95cc965bfdf4ec48fd7cc51b1c56b2f.jpg', '2024-05-05 20:56:25', '2024-05-05 20:56:25', 1, 1);
INSERT INTO `notice` VALUES (7, 1, '部分学生通知21328', '部分学生哈哈哈哈哈1328', '300ce133a353420ead6dd65024ec7081.jpg', '2024-05-05 20:57:27', '2024-05-06 13:29:11', 1, 2);
INSERT INTO `notice` VALUES (8, 1, 'hello', '你哈哈哈哈', '9ed1b7a1453748aea579683732ce6564.txt', '2024-05-06 13:33:05', '2024-05-06 13:33:05', 1, 1);
INSERT INTO `notice` VALUES (9, 1, '49955', '53676vv', '56c759e4798041c18052590a370a0c8f.jpg', '2024-05-06 13:35:32', '2024-05-06 13:36:42', 1, 1);
INSERT INTO `notice` VALUES (10, 1, '法人股太皇太后', '成都v根本不敢不敢播放的版本', '0b16a9bdddf84674a118039027589160.jpg', '2024-05-06 18:27:18', '2024-05-06 18:27:24', 0, 2);
INSERT INTO `notice` VALUES (11, 1, 'pdf', 'pdfpdf', 'd5e98be93a5c494aad64cc4fe6694539.pdf', '2024-05-07 07:19:27', '2024-05-07 07:19:27', 1, 1);
INSERT INTO `notice` VALUES (12, 1, 'vv无法绕过', '凑热闹特和特殊', '74d93bd4938349018623f674c15c61f7.txt', '2024-05-08 14:19:43', '2024-05-08 14:19:43', 1, 2);
INSERT INTO `notice` VALUES (13, 1, '吃饭吧', '我跟', '7f7a459865474c9fb3a0f32f71b3f3d7.pdf', '2024-05-08 14:21:19', '2024-05-08 14:21:19', 1, 2);
INSERT INTO `notice` VALUES (14, 3, 'aaa', 'dvbg', 'c05c46d1a6ea4aaeb486aceb71619392.pdf', '2024-05-09 11:00:08', '2024-05-09 11:00:08', 1, 1);
INSERT INTO `notice` VALUES (15, 3, 'feretgf', 'fregthytu', 'c05c46d1a6ea4aaeb486aceb71619392.pdf', '2024-05-09 11:00:21', '2024-05-10 10:59:19', 1, 2);
INSERT INTO `notice` VALUES (16, 1, '发个通告', '风格灌灌灌灌', 'a1c253564a15441c8da59f18e8008da7.jpeg', '2024-05-11 17:56:59', '2024-05-11 17:56:59', 1, 2);

-- ----------------------------
-- Table structure for student_assignment
-- ----------------------------
DROP TABLE IF EXISTS `student_assignment`;
CREATE TABLE `student_assignment`  (
  `id` bigint(0) NOT NULL AUTO_INCREMENT,
  `student_id` bigint(0) NULL DEFAULT NULL COMMENT '学生id',
  `assignment_id` bigint(0) NULL DEFAULT NULL COMMENT '作业id',
  `file_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '文件名',
  `score` int(0) NULL DEFAULT NULL COMMENT '分数',
  `feedback` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '老师反馈评价',
  `status` tinyint(0) NULL DEFAULT 0 COMMENT '0未提交 1已提交 2已批改',
  `create_time` datetime(0) NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime(0) NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP(0) COMMENT '修改时间',
  `state` tinyint(0) NULL DEFAULT 1 COMMENT '1正常 0删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 9 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '学生作业表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of student_assignment
-- ----------------------------
INSERT INTO `student_assignment` VALUES (1, 2, 1, '0b16a9bdddf84674a118039027589160.jpg', 78, '还不错', 2, '2024-05-08 17:31:51', '2024-05-09 19:52:01', 1);
INSERT INTO `student_assignment` VALUES (2, 2, 2, '0cf0bdee99834cd683bbfc9778b7d02c.doc', 56, '彻底否认', 2, '2024-05-08 17:31:59', '2024-05-09 19:54:44', 1);
INSERT INTO `student_assignment` VALUES (3, 2, 3, '7f7a459865474c9fb3a0f32f71b3f3d7.pdf', 99, '666', 2, '2024-05-08 17:32:04', '2024-05-09 19:55:31', 1);
INSERT INTO `student_assignment` VALUES (4, 4, 1, '9ed1b7a1453748aea579683732ce6564.txt', 78, '还不错', 2, '2024-05-08 17:32:09', '2024-05-11 17:59:14', 1);
INSERT INTO `student_assignment` VALUES (5, 4, 2, '9ed1b7a1453748aea579683732ce6564.txt', NULL, NULL, 1, '2024-05-08 17:32:13', '2024-05-09 17:54:45', 1);
INSERT INTO `student_assignment` VALUES (6, 4, 3, NULL, NULL, NULL, 1, '2024-05-08 17:32:18', '2024-05-08 17:47:47', 1);
INSERT INTO `student_assignment` VALUES (7, 2, 7, '6ceb7bf021264ff9b9706bdc3bf5898c.doc', NULL, NULL, 1, '2024-05-10 18:01:56', '2024-05-11 08:06:26', 1);
INSERT INTO `student_assignment` VALUES (8, 4, 7, NULL, NULL, NULL, 0, '2024-05-10 18:01:56', '2024-05-10 18:01:56', 1);

-- ----------------------------
-- Table structure for student_course
-- ----------------------------
DROP TABLE IF EXISTS `student_course`;
CREATE TABLE `student_course`  (
  `id` bigint(0) NOT NULL AUTO_INCREMENT,
  `student_id` bigint(0) NULL DEFAULT NULL COMMENT '学生id',
  `course_id` bigint(0) NULL DEFAULT NULL COMMENT '课程id',
  `create_time` datetime(0) NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime(0) NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP(0) COMMENT '修改时间',
  `state` tinyint(0) NULL DEFAULT 1 COMMENT '1正常 0删除',
  `status` tinyint(0) NULL DEFAULT 0 COMMENT '选课状态：0未通过 1已通过',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '学生选课表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of student_course
-- ----------------------------
INSERT INTO `student_course` VALUES (1, 2, 1, '2024-05-06 17:19:52', '2024-05-07 11:20:41', 1, 1);
INSERT INTO `student_course` VALUES (2, 4, 1, '2024-05-06 17:20:10', '2024-05-07 11:40:29', 1, 1);
INSERT INTO `student_course` VALUES (3, 5, 1, '2024-05-06 17:20:17', '2024-05-07 11:39:57', 1, 0);
INSERT INTO `student_course` VALUES (4, 8, 5, '2024-05-06 17:20:33', '2024-05-08 16:39:46', 1, 1);
INSERT INTO `student_course` VALUES (5, 2, 8, '2024-05-10 13:58:13', '2024-05-10 13:58:13', 1, 0);
INSERT INTO `student_course` VALUES (6, 2, 9, '2024-05-10 14:47:25', '2024-05-10 14:47:25', 1, 0);
INSERT INTO `student_course` VALUES (7, 2, 10, '2024-05-11 18:00:46', '2024-05-11 18:01:59', 1, 1);

-- ----------------------------
-- Table structure for student_lecture
-- ----------------------------
DROP TABLE IF EXISTS `student_lecture`;
CREATE TABLE `student_lecture`  (
  `id` bigint(0) NOT NULL AUTO_INCREMENT,
  `student_id` bigint(0) NULL DEFAULT NULL COMMENT '学生id',
  `lecture_id` bigint(0) NULL DEFAULT NULL COMMENT '讲座id',
  `create_time` datetime(0) NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime(0) NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP(0) COMMENT '修改时间',
  `state` tinyint(0) NULL DEFAULT 1 COMMENT '1正常 0删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '学生讲座表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of student_lecture
-- ----------------------------
INSERT INTO `student_lecture` VALUES (1, 2, 4, '2024-05-09 15:41:59', '2024-05-09 15:49:07', 0);
INSERT INTO `student_lecture` VALUES (2, 4, 4, '2024-05-09 15:41:59', '2024-05-09 15:49:07', 0);
INSERT INTO `student_lecture` VALUES (3, 2, 1, '2024-05-09 15:42:54', '2024-05-09 15:50:48', 0);
INSERT INTO `student_lecture` VALUES (4, 6, 1, '2024-05-09 15:42:54', '2024-05-09 15:50:48', 0);
INSERT INTO `student_lecture` VALUES (5, 8, 1, '2024-05-09 15:42:54', '2024-05-09 15:50:48', 0);
INSERT INTO `student_lecture` VALUES (6, 13, 1, '2024-05-09 15:42:54', '2024-05-09 15:50:48', 0);
INSERT INTO `student_lecture` VALUES (7, 5, 4, '2024-05-09 15:49:07', '2024-05-09 15:49:07', 1);

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `id` bigint(0) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '用户名',
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '密码',
  `number_id` bigint(0) NULL DEFAULT NULL COMMENT '学号或工号',
  `role` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '角色：admin instructor student',
  `status` tinyint(0) NULL DEFAULT 1 COMMENT '状态：0禁用 1正常',
  `create_time` datetime(0) NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime(0) NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP(0) COMMENT '修改时间',
  `state` tinyint(0) NULL DEFAULT 1 COMMENT '1正常 0删除',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `uni_username`(`username`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 19 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '用户表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES (1, 'admin', 'e10adc3949ba59abbe56e057f20f883e', 10000, 'admin', 1, '2024-05-02 16:21:13', '2024-05-11 17:33:46', 1);
INSERT INTO `user` VALUES (2, '猪小明', '4297f44b13955235245b2497399d7a93', 30001, 'student', 1, '2024-05-02 16:21:43', '2024-05-11 17:51:11', 1);
INSERT INTO `user` VALUES (3, '李教授', '25d55ad283aa400af464c76d713c07ad', 20001, 'instructor', 1, '2024-05-02 16:22:24', '2024-05-11 17:52:05', 1);
INSERT INTO `user` VALUES (4, '蘑菇头2', 'e10adc3949ba59abbe56e057f20f883e', 30002, 'student', 1, '2024-05-04 07:36:34', '2024-05-07 08:45:05', 1);
INSERT INTO `user` VALUES (5, '米线', 'e10adc3949ba59abbe56e057f20f883e', 30003, 'student', 0, '2024-05-04 07:36:52', '2024-05-11 17:54:59', 0);
INSERT INTO `user` VALUES (6, 'ggbong', 'e10adc3949ba59abbe56e057f20f883e', 30004, 'student', 1, '2024-05-04 07:37:27', '2024-05-04 07:40:50', 1);
INSERT INTO `user` VALUES (7, '美羊羊', 'e10adc3949ba59abbe56e057f20f883e', 30005, 'student', 1, '2024-05-04 07:37:41', '2024-05-06 15:56:04', 0);
INSERT INTO `user` VALUES (8, '沸羊羊', 'e10adc3949ba59abbe56e057f20f883e', 30006, 'student', 1, '2024-05-04 07:38:29', '2024-05-06 17:22:47', 1);
INSERT INTO `user` VALUES (9, '张老师', 'e10adc3949ba59abbe56e057f20f883e', 20002, 'instructor', 1, '2024-05-04 07:38:44', '2024-05-04 07:41:26', 1);
INSERT INTO `user` VALUES (10, '王老师', 'e10adc3949ba59abbe56e057f20f883e', 20003, 'instructor', 1, '2024-05-04 07:39:11', '2024-05-04 07:41:30', 1);
INSERT INTO `user` VALUES (11, '张三丰w', 'e10adc3949ba59abbe56e057f20f883e', 30054, 'student', 1, '2024-05-06 15:56:38', '2024-05-06 16:44:40', 0);
INSERT INTO `user` VALUES (12, 'jerrydd', 'e10adc3949ba59abbe56e057f20f883e', 10089, 'student', 1, '2024-05-06 16:31:17', '2024-05-06 16:43:44', 0);
INSERT INTO `user` VALUES (13, 'dffbgnhg', 'e10adc3949ba59abbe56e057f20f883e', 132345, 'student', 1, '2024-05-06 16:35:04', '2024-05-06 16:44:19', 1);
INSERT INTO `user` VALUES (14, 'erdsvds', 'e10adc3949ba59abbe56e057f20f883e', 4546, 'student', 0, '2024-05-06 16:44:53', '2024-05-07 10:15:01', 0);
INSERT INTO `user` VALUES (15, 'df', 'e10adc3949ba59abbe56e057f20f883e', 566786, 'student', 1, '2024-05-06 16:46:02', '2024-05-06 16:46:24', 1);
INSERT INTO `user` VALUES (16, 'fregtr', 'e10adc3949ba59abbe56e057f20f883e', 456, 'student', 0, '2024-05-06 16:46:10', '2024-05-07 11:33:07', 0);
INSERT INTO `user` VALUES (17, '发给他人', 'e10adc3949ba59abbe56e057f20f883e', 45, 'student', 1, '2024-05-06 18:26:32', '2024-05-07 10:09:07', 0);
INSERT INTO `user` VALUES (18, '刘老师', 'e10adc3949ba59abbe56e057f20f883e', 20005, 'instructor', 0, '2024-05-07 13:15:01', '2024-05-07 13:15:27', 0);

-- ----------------------------
-- Table structure for user_notice
-- ----------------------------
DROP TABLE IF EXISTS `user_notice`;
CREATE TABLE `user_notice`  (
  `id` bigint(0) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(0) NULL DEFAULT NULL COMMENT '用户id',
  `notice_id` bigint(0) NULL DEFAULT NULL COMMENT '通知id',
  `create_time` datetime(0) NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime(0) NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP(0) COMMENT '修改时间',
  `state` tinyint(0) NULL DEFAULT 1 COMMENT '1正常 0删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 34 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '用户通知表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user_notice
-- ----------------------------
INSERT INTO `user_notice` VALUES (1, 2, 7, '2024-05-05 20:57:27', '2024-05-06 10:50:36', 0);
INSERT INTO `user_notice` VALUES (2, 4, 7, '2024-05-05 20:57:27', '2024-05-06 10:50:36', 0);
INSERT INTO `user_notice` VALUES (3, 5, 7, '2024-05-05 20:57:27', '2024-05-06 10:50:36', 0);
INSERT INTO `user_notice` VALUES (4, 6, 7, '2024-05-05 20:57:27', '2024-05-06 10:50:36', 0);
INSERT INTO `user_notice` VALUES (5, 2, 1, '2024-05-06 10:42:42', '2024-05-06 10:43:53', 0);
INSERT INTO `user_notice` VALUES (6, 3, 1, '2024-05-06 10:42:42', '2024-05-06 10:43:53', 0);
INSERT INTO `user_notice` VALUES (7, 4, 1, '2024-05-06 10:42:42', '2024-05-06 10:43:53', 0);
INSERT INTO `user_notice` VALUES (8, 5, 1, '2024-05-06 10:42:42', '2024-05-06 10:43:53', 0);
INSERT INTO `user_notice` VALUES (9, 7, 1, '2024-05-06 10:43:53', '2024-05-06 10:54:13', 0);
INSERT INTO `user_notice` VALUES (10, 8, 1, '2024-05-06 10:43:53', '2024-05-06 10:54:13', 0);
INSERT INTO `user_notice` VALUES (11, 2, 7, '2024-05-06 10:50:36', '2024-05-06 13:29:11', 0);
INSERT INTO `user_notice` VALUES (12, 4, 7, '2024-05-06 10:50:36', '2024-05-06 13:29:11', 0);
INSERT INTO `user_notice` VALUES (13, 5, 7, '2024-05-06 10:50:36', '2024-05-06 13:29:11', 0);
INSERT INTO `user_notice` VALUES (14, 6, 7, '2024-05-06 10:50:36', '2024-05-06 13:29:11', 0);
INSERT INTO `user_notice` VALUES (15, 1, 2, '2024-05-06 10:56:21', '2024-05-06 10:57:20', 0);
INSERT INTO `user_notice` VALUES (16, 2, 2, '2024-05-06 10:56:21', '2024-05-06 10:57:20', 0);
INSERT INTO `user_notice` VALUES (17, 9, 2, '2024-05-06 10:58:32', '2024-05-06 11:00:59', 0);
INSERT INTO `user_notice` VALUES (18, 10, 2, '2024-05-06 10:58:32', '2024-05-06 11:00:59', 0);
INSERT INTO `user_notice` VALUES (19, 3, 2, '2024-05-06 11:00:59', '2024-05-06 11:02:08', 0);
INSERT INTO `user_notice` VALUES (20, 4, 2, '2024-05-06 11:00:59', '2024-05-06 11:02:08', 0);
INSERT INTO `user_notice` VALUES (21, 3, 2, '2024-05-06 11:02:08', '2024-05-06 18:27:44', 0);
INSERT INTO `user_notice` VALUES (22, 10, 7, '2024-05-06 13:29:11', '2024-05-06 13:29:11', 1);
INSERT INTO `user_notice` VALUES (23, 4, 9, '2024-05-06 13:35:32', '2024-05-06 13:36:42', 0);
INSERT INTO `user_notice` VALUES (24, 9, 9, '2024-05-06 13:35:32', '2024-05-06 13:36:42', 0);
INSERT INTO `user_notice` VALUES (25, 2, 10, '2024-05-06 18:27:18', '2024-05-06 18:27:24', 0);
INSERT INTO `user_notice` VALUES (26, 3, 10, '2024-05-06 18:27:18', '2024-05-06 18:27:24', 0);
INSERT INTO `user_notice` VALUES (27, 5, 10, '2024-05-06 18:27:18', '2024-05-06 18:27:24', 0);
INSERT INTO `user_notice` VALUES (28, 2, 12, '2024-05-08 14:19:43', '2024-05-08 14:19:43', 1);
INSERT INTO `user_notice` VALUES (29, 4, 13, '2024-05-08 14:21:19', '2024-05-08 14:21:19', 1);
INSERT INTO `user_notice` VALUES (30, 2, 15, '2024-05-09 11:00:21', '2024-05-09 11:00:39', 0);
INSERT INTO `user_notice` VALUES (31, 4, 15, '2024-05-09 11:00:21', '2024-05-09 11:00:39', 0);
INSERT INTO `user_notice` VALUES (32, 2, 15, '2024-05-09 11:00:39', '2024-05-09 11:00:39', 1);
INSERT INTO `user_notice` VALUES (33, 4, 15, '2024-05-09 11:00:39', '2024-05-09 11:00:39', 1);
INSERT INTO `user_notice` VALUES (34, 2, 16, '2024-05-11 17:56:59', '2024-05-11 17:56:59', 1);
INSERT INTO `user_notice` VALUES (35, 3, 16, '2024-05-11 17:56:59', '2024-05-11 17:56:59', 1);
INSERT INTO `user_notice` VALUES (36, 4, 16, '2024-05-11 17:56:59', '2024-05-11 17:56:59', 1);
INSERT INTO `user_notice` VALUES (37, 6, 16, '2024-05-11 17:56:59', '2024-05-11 17:56:59', 1);

SET FOREIGN_KEY_CHECKS = 1;
