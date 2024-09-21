SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for wait_article
-- ----------------------------
DROP TABLE IF EXISTS `wait_article`;
CREATE TABLE `wait_article` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  `cid` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '类目',
  `title` varchar(100) NOT NULL DEFAULT '' COMMENT '标题',
  `image` varchar(200) NOT NULL DEFAULT '' COMMENT '封面',
  `intro` varchar(200) NOT NULL DEFAULT '' COMMENT '简介',
  `content` text COMMENT '内容',
  `browse` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '浏览',
  `collect` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '收藏',
  `sort` smallint(5) unsigned NOT NULL DEFAULT '0' COMMENT '排序',
  `is_topping` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '是否置顶: [0=否, 1=是]',
  `is_recommend` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '是否推荐: [0=否, 1=是]',
  `is_show` tinyint(255) unsigned NOT NULL DEFAULT '0' COMMENT '是否显示: [0=否, 1=是]',
  `is_delete` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '是否删除: [0=否, 1=是]',
  `create_time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '创建时间',
  `update_time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '更新时间',
  `delete_time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '删除时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='文章内容表';

-- ----------------------------
-- Table structure for wait_article_category
-- ----------------------------
DROP TABLE IF EXISTS `wait_article_category`;
CREATE TABLE `wait_article_category` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  `name` varchar(20) NOT NULL DEFAULT '' COMMENT '类目名称',
  `sort` smallint(5) unsigned NOT NULL DEFAULT '0' COMMENT '类目排序',
  `is_disable` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '是否禁用: [0=否, 1=是]',
  `is_delete` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '是否删除: [0=否, 1=是]',
  `create_time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '创建时间',
  `update_time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '更新时间',
  `delete_time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '删除时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='文章类目表';

-- ----------------------------
-- Table structure for wait_article_collect
-- ----------------------------
DROP TABLE IF EXISTS `wait_article_collect`;
CREATE TABLE `wait_article_collect` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  `user_id` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '用户ID',
  `article_id` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '文章ID',
  `is_delete` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '是否删除: [0=否, 1=是]',
  `create_time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '创建时间',
  `update_time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '更新时间',
  `delete_time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '删除时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='用户收藏表';

-- ----------------------------
-- Table structure for wait_attach
-- ----------------------------
DROP TABLE IF EXISTS `wait_attach`;
CREATE TABLE `wait_attach` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  `uid` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '用户ID',
  `cid` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '分类ID',
  `file_type` tinyint(2) unsigned NOT NULL DEFAULT '10' COMMENT '文件类型: [10=图片, 20=视频, 30=压缩, 40=文件]',
  `file_name` varchar(200) NOT NULL DEFAULT '' COMMENT '文件名称',
  `file_path` varchar(200) NOT NULL DEFAULT '' COMMENT '文件路径',
  `file_ext` varchar(10) NOT NULL DEFAULT '' COMMENT '文件扩展',
  `file_size` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '文件大小',
  `is_user` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '用户上传: [0=否, 1=是]',
  `is_attach` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '仓库附件: [0=否, 1=是]',
  `is_delete` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '是否删除: [0=否, 1=是]',
  `create_time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '创建时间',
  `update_time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '更新时间',
  `delete_time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '删除时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='附件文件表';

-- ----------------------------
-- Table structure for wait_attach_cate
-- ----------------------------
DROP TABLE IF EXISTS `wait_attach_cate`;
CREATE TABLE `wait_attach_cate` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  `name` varchar(20) NOT NULL DEFAULT '' COMMENT '分类名称',
  `type` tinyint(2) unsigned NOT NULL DEFAULT '10' COMMENT '分类类型: [10=图片, 20=视频, 30=压缩, 40=文件]',
  `is_delete` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '是否删除: [0=否, 1=是]',
  `create_time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '创建时间',
  `update_time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '更新时间',
  `delete_time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '删除时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='附件类目表';

-- ----------------------------
-- Table structure for wait_auth_admin
-- ----------------------------
DROP TABLE IF EXISTS `wait_auth_admin`;
CREATE TABLE `wait_auth_admin` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  `role_id` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '账号角色',
  `dept_id` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '部门主键',
  `post_id` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '岗位主键',
  `nickname` varchar(32) NOT NULL DEFAULT '' COMMENT '账号昵称',
  `username` varchar(32) NOT NULL DEFAULT '' COMMENT '登录账号',
  `password` varchar(32) NOT NULL DEFAULT '' COMMENT '登录密码',
  `salt` varchar(32) NOT NULL DEFAULT '' COMMENT '加密盐巴',
  `avatar` varchar(200) NOT NULL DEFAULT '' COMMENT '用户头像',
  `mobile` varchar(100) NOT NULL DEFAULT '' COMMENT '用户电话',
  `email` varchar(100) NOT NULL DEFAULT '' COMMENT '电子邮箱',
  `last_login_ip` varchar(100) NOT NULL DEFAULT '' COMMENT '登录地址',
  `last_login_time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '登录时间',
  `is_disable` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '是否禁用: [0=否, 1=是]',
  `is_delete` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '是否删除: [0=否, 1=是]',
  `create_time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '创建时间',
  `update_time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '更新时间',
  `delete_time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '删除时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='用户管理表';

-- ----------------------------
-- Table structure for wait_auth_dept
-- ----------------------------
DROP TABLE IF EXISTS `wait_auth_dept`;
CREATE TABLE `wait_auth_dept` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  `pid` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '上级主键',
  `name` varchar(100) NOT NULL DEFAULT '' COMMENT '部门名称',
  `duty` varchar(30) NOT NULL DEFAULT '' COMMENT '负责人名',
  `mobile` varchar(30) NOT NULL DEFAULT '' COMMENT '部门电话',
  `sort` smallint(5) unsigned NOT NULL DEFAULT '0' COMMENT '排序编号',
  `level` smallint(5) unsigned NOT NULL DEFAULT '1' COMMENT '关系层级',
  `relation` varchar(500) NOT NULL DEFAULT '' COMMENT '关系链条',
  `is_disable` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '是否禁用: [0=否, 1=是]',
  `is_delete` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '是否删除: [0=否, 1=是]',
  `create_time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '创建时间',
  `update_time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '更新时间',
  `delete_time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '删除时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='部门管理表';

-- ----------------------------
-- Table structure for wait_auth_menu
-- ----------------------------
DROP TABLE IF EXISTS `wait_auth_menu`;
CREATE TABLE `wait_auth_menu` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  `pid` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '菜单父级',
  `type` char(1) NOT NULL DEFAULT '' COMMENT '权限类型: [M=目录, C=菜单, A=按钮]',
  `name` varchar(100) NOT NULL DEFAULT '' COMMENT '菜单名称',
  `icon` varchar(100) NOT NULL DEFAULT '' COMMENT '菜单图标',
  `sort` smallint(5) unsigned NOT NULL DEFAULT '0' COMMENT '菜单排序',
  `perms` varchar(100) NOT NULL DEFAULT '' COMMENT '菜单权限',
  `params` varchar(200) NOT NULL DEFAULT '' COMMENT '路由参数',
  `component` varchar(200) NOT NULL DEFAULT '' COMMENT '组件路径',
  `path` varchar(200) NOT NULL DEFAULT '' COMMENT '页面路径',
  `is_show` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '是否显示: [0=否, 1=是]',
  `is_disable` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '是否禁用: [0=否, 1=是]',
  `is_delete` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '是否删除: [0=否, 1=是]',
  `create_time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '创建时间',
  `update_time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '更新时间',
  `delete_time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '删除时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='菜单管理表';

-- ----------------------------
-- Table structure for wait_auth_perm
-- ----------------------------
DROP TABLE IF EXISTS `wait_auth_perm`;
CREATE TABLE `wait_auth_perm` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  `role_id` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '角色主键',
  `menu_id` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '菜单主键',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='权限管理表';

-- ----------------------------
-- Table structure for wait_auth_post
-- ----------------------------
DROP TABLE IF EXISTS `wait_auth_post`;
CREATE TABLE `wait_auth_post` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  `code` varchar(30) NOT NULL DEFAULT '' COMMENT '岗位编码',
  `name` varchar(30) NOT NULL DEFAULT '' COMMENT '岗位名称',
  `remarks` varchar(200) NOT NULL DEFAULT '' COMMENT '岗位备注',
  `sort` smallint(5) unsigned NOT NULL DEFAULT '0' COMMENT '岗位排序',
  `is_disable` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '是否禁用: [0=否, 1=是]',
  `is_delete` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '是否删除: [0=否, 1=是]',
  `create_time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '创建时间',
  `update_time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '更新时间',
  `delete_time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '删除时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='岗位管理表';

-- ----------------------------
-- Table structure for wait_auth_role
-- ----------------------------
DROP TABLE IF EXISTS `wait_auth_role`;
CREATE TABLE `wait_auth_role` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  `name` varchar(20) CHARACTER SET utf16 NOT NULL DEFAULT '' COMMENT '角色名称',
  `describe` varchar(200) NOT NULL DEFAULT '' COMMENT '角色描述',
  `sort` smallint(5) unsigned NOT NULL DEFAULT '0' COMMENT '角色排序',
  `is_disable` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '是否禁用: [0=否, 1=是]',
  `is_delete` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '是否删除: [0=否, 1=是]',
  `create_time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '创建时间',
  `update_time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '更新时间',
  `delete_time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '删除时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='角色管理表';

-- ----------------------------
-- Table structure for wait_dev_banner
-- ----------------------------
DROP TABLE IF EXISTS `wait_dev_banner`;
CREATE TABLE `wait_dev_banner` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  `position` tinyint(2) unsigned NOT NULL DEFAULT '0' COMMENT '轮播位置',
  `title` varchar(200) NOT NULL DEFAULT '' COMMENT '轮播标题',
  `image` varchar(250) NOT NULL DEFAULT '' COMMENT '轮播图片',
  `target` varchar(250) NOT NULL DEFAULT '' COMMENT '跳转方式',
  `url` varchar(250) NOT NULL DEFAULT '' COMMENT '跳转链接',
  `sort` smallint(5) unsigned NOT NULL DEFAULT '0' COMMENT '排序编号',
  `is_disable` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '是否禁用: [0=否, 1=是]',
  `is_delete` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '是否删除: [0=否, 1=是]',
  `create_time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '创建时间',
  `update_time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '更新时间',
  `delete_time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '删除时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='轮播管理表';

-- ----------------------------
-- Table structure for wait_dev_links
-- ----------------------------
DROP TABLE IF EXISTS `wait_dev_links`;
CREATE TABLE `wait_dev_links` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  `title` varchar(200) NOT NULL DEFAULT '' COMMENT '友链名称',
  `image` varchar(250) NOT NULL DEFAULT '' COMMENT '友链图标',
  `target` varchar(250) NOT NULL DEFAULT '' COMMENT '跳转方式',
  `url` varchar(250) NOT NULL DEFAULT '' COMMENT '跳转链接',
  `sort` smallint(5) unsigned NOT NULL DEFAULT '0' COMMENT '排序编号',
  `is_disable` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '是否禁用: [0=否, 1=是]',
  `is_delete` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '是否删除: [0=否, 1=是]',
  `create_time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '创建时间',
  `update_time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '更新时间',
  `delete_time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '删除时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='友链管理表';

-- ----------------------------
-- Table structure for wait_dev_pay_config
-- ----------------------------
DROP TABLE IF EXISTS `wait_dev_pay_config`;
CREATE TABLE `wait_dev_pay_config` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `channel` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '支付渠道',
  `shorter` varchar(32) NOT NULL DEFAULT '' COMMENT '简写名称',
  `name` varchar(32) NOT NULL DEFAULT '' COMMENT '渠道名称',
  `logo` varchar(250) NOT NULL DEFAULT '' COMMENT '渠道图标',
  `icon` varchar(250) NOT NULL DEFAULT '' COMMENT '支付图标',
  `params` text COMMENT '支付参数',
  `sort` int(5) unsigned NOT NULL DEFAULT '0' COMMENT '排序编号',
  `status` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '渠道状态: [0=禁用, 1=启用]',
  `create_time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '创建时间',
  `update_time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='支付配置表';

-- ----------------------------
-- Table structure for wait_notice_record
-- ----------------------------
DROP TABLE IF EXISTS `wait_notice_record`;
CREATE TABLE `wait_notice_record` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  `scene` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '通知场景',
  `user_id` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '接收用户',
  `account` varchar(100) NOT NULL DEFAULT '' COMMENT '接收账号',
  `title` varchar(100) NOT NULL DEFAULT '' COMMENT '通知标题',
  `code` varchar(10) NOT NULL DEFAULT '' COMMENT '验证编码',
  `content` text COMMENT '通知内容',
  `error` text COMMENT '失败原因',
  `sender` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '发送类型: [1=系统, 2=邮件, 3=短信, 4=公众号, 5=小程序]',
  `receiver` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '接收对象: [1=用户, 2=平台]',
  `status` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '通知状态: [0=等待, 1=成功, 2=失败]',
  `is_read` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '已读状态: [0=未读, 1=已读]',
  `is_captcha` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '是验证码: [0=否的, 1=是的]',
  `is_delete` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '是否删除: [0=否的, 1=是的]',
  `expire_time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '失效时间',
  `create_time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '创建时间',
  `update_time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '更新时间',
  `delete_time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '删除时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='通知记录表';

-- ----------------------------
-- Table structure for wait_notice_setting
-- ----------------------------
DROP TABLE IF EXISTS `wait_notice_setting`;
CREATE TABLE `wait_notice_setting` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  `scene` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '场景编码',
  `name` varchar(100) NOT NULL DEFAULT '' COMMENT '场景名称',
  `remarks` varchar(200) NOT NULL DEFAULT '' COMMENT '场景描述',
  `variable` text COMMENT '场景变量',
  `sys_template` text COMMENT '系统通知模板',
  `sms_template` text COMMENT '短信通知模板',
  `ems_template` text COMMENT '邮件通知模板',
  `get_client` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '接收端口: [1=用户, 2=平台]',
  `is_captcha` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '是验证码: [0=否的, 1=是的]',
  `is_delete` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '是否删除: [0=否的, 1=是的]',
  `create_time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '创建时间',
  `update_time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '更新时间',
  `delete_time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '删除时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='通知设置表';

-- ----------------------------
-- Table structure for wait_recharge_order
-- ----------------------------
DROP TABLE IF EXISTS `wait_recharge_order`;
CREATE TABLE `wait_recharge_order` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `user_id` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '用户ID',
  `order_sn` varchar(64) NOT NULL DEFAULT '' COMMENT '订单编号',
  `terminal` tinyint(1) unsigned NOT NULL DEFAULT '1' COMMENT '来源平台: [1=微信小程序, 2=微信公众号, 3=H5, 4=PC, 5=安卓, 5=苹果]',
  `pay_way` tinyint(1) unsigned NOT NULL DEFAULT '2' COMMENT '支付方式: [2=微信支付，3=支付宝支付]',
  `pay_status` tinyint(1) NOT NULL DEFAULT '0' COMMENT '支付状态: [0=待支付，1=已支付]',
  `package_id` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '充值套餐',
  `transaction_id` varchar(64) NOT NULL DEFAULT '' COMMENT '支付流水号',
  `paid_amount` decimal(8,2) unsigned NOT NULL DEFAULT '0.00' COMMENT '充值金额',
  `give_amount` decimal(8,2) unsigned NOT NULL DEFAULT '0.00' COMMENT '赠送金额',
  `is_delete` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '是否删除: [0=否, 1=是]',
  `pay_time` int(10) NOT NULL DEFAULT '0' COMMENT '支付时间',
  `create_time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '创建时间',
  `update_time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '更新时间',
  `delete_time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '删除时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='充值订单表';

-- ----------------------------
-- Table structure for wait_recharge_package
-- ----------------------------
DROP TABLE IF EXISTS `wait_recharge_package`;
CREATE TABLE `wait_recharge_package` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `name` varchar(100) NOT NULL DEFAULT '' COMMENT '套餐名称',
  `money` decimal(8,2) unsigned NOT NULL DEFAULT '0.00' COMMENT '充值金额',
  `give_money` decimal(8,2) unsigned NOT NULL DEFAULT '0.00' COMMENT '赠送金额',
  `sort` smallint(5) unsigned NOT NULL DEFAULT '0' COMMENT '排序',
  `is_show` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '是否显示: 0=否, 1=是',
  `is_delete` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '是否删除: 0=否, 1=是',
  `create_time` int(10) unsigned DEFAULT NULL COMMENT '创建时间',
  `update_time` int(10) unsigned DEFAULT NULL COMMENT '更新时间',
  `delete_time` int(10) unsigned DEFAULT NULL COMMENT '删除时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='充值套餐表';

-- ----------------------------
-- Table structure for wait_sys_config
-- ----------------------------
DROP TABLE IF EXISTS `wait_sys_config`;
CREATE TABLE `wait_sys_config` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  `type` varchar(100) NOT NULL DEFAULT '' COMMENT '类型',
  `key` varchar(100) NOT NULL DEFAULT '' COMMENT '键名',
  `value` text COMMENT '键值',
  `remarks` varchar(100) NOT NULL DEFAULT '' COMMENT '备注',
  `create_time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '创建时间',
  `update_time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='系统配置表';

-- ----------------------------
-- Table structure for wait_sys_crontab
-- ----------------------------
DROP TABLE IF EXISTS `wait_sys_crontab`;
CREATE TABLE `wait_sys_crontab` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `name` varchar(64) NOT NULL DEFAULT '' COMMENT '任务名称',
  `command` varchar(200) NOT NULL DEFAULT '' COMMENT '执行命令',
  `params` varchar(200) NOT NULL DEFAULT '' COMMENT '附带参数',
  `trigger` varchar(100) NOT NULL DEFAULT '' COMMENT '触发类型',
  `rules` text COMMENT '运行规则',
  `concurrent` tinyint(2) unsigned NOT NULL DEFAULT '1' COMMENT '并发数量',
  `remarks` varchar(300) NOT NULL DEFAULT '' COMMENT '备注信息',
  `error` text COMMENT '错误提示',
  `status` tinyint(1) unsigned NOT NULL DEFAULT '1' COMMENT '执行状态: [1=运行, 2=暂停, 3=错误]',
  `exe_time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '执行时长',
  `max_time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '最大执行时长',
  `last_time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '最后执行时间',
  `is_delete` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '是否删除: [0=否, 1=是]',
  `create_time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '创建时间',
  `update_time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '更新时间',
  `delete_time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '删除时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='系统任务表';

-- ----------------------------
-- Table structure for wait_sys_log
-- ----------------------------
DROP TABLE IF EXISTS `wait_sys_log`;
CREATE TABLE `wait_sys_log` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  `admin_id` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '操作人员',
  `summary` varchar(100) NOT NULL DEFAULT '' COMMENT '摘要信息',
  `endpoint` varchar(300) NOT NULL DEFAULT '' COMMENT '执行函数',
  `method` varchar(30) NOT NULL DEFAULT '' COMMENT '请求方法',
  `url` varchar(100) NOT NULL DEFAULT '' COMMENT '请求路由',
  `ip` varchar(100) NOT NULL DEFAULT '' COMMENT '请求IP',
  `ua` varchar(100) NOT NULL DEFAULT '' COMMENT '请求UA',
  `user_agent` varchar(900) NOT NULL DEFAULT '' COMMENT 'UA详情',
  `params` longtext COMMENT '请求参数',
  `error` longtext COMMENT '错误信息',
  `status` tinyint(1) unsigned NOT NULL DEFAULT '1' COMMENT '执行状态: 1=成功, 2=失败',
  `start_time` varchar(20) NOT NULL DEFAULT '0' COMMENT '开始时间: 毫秒',
  `end_time` varchar(20) NOT NULL DEFAULT '0' COMMENT '结束时间: 毫秒',
  `task_time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '耗时时间: 毫秒',
  `create_time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '操作时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='系统日志表';

-- ----------------------------
-- Table structure for wait_user
-- ----------------------------
DROP TABLE IF EXISTS `wait_user`;
CREATE TABLE `wait_user` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  `group_id` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '用户分组',
  `sn` varchar(20) NOT NULL DEFAULT '' COMMENT '用户编号',
  `account` varchar(32) NOT NULL DEFAULT '' COMMENT '用户账号',
  `password` varchar(32) NOT NULL DEFAULT '' COMMENT '登录密码',
  `nickname` varchar(32) NOT NULL DEFAULT '' COMMENT '用户名称',
  `avatar` varchar(200) NOT NULL DEFAULT '' COMMENT '用户头像',
  `salt` varchar(32) NOT NULL DEFAULT '' COMMENT '加密盐巴',
  `gender` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '用户性别',
  `mobile` varchar(20) NOT NULL DEFAULT '' COMMENT '手机号码',
  `email` varchar(100) NOT NULL DEFAULT '' COMMENT '电子邮箱',
  `balance` decimal(10,2) NOT NULL DEFAULT '0.00' COMMENT '钱包余额',
  `last_login_ip` varchar(100) NOT NULL DEFAULT '' COMMENT '最后登录IP',
  `last_login_time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '最后登录时间',
  `is_disable` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '是否禁用: [0=否, 1=是]',
  `is_delete` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '是否删除: [0=否, 1=是]',
  `create_time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '创建时间',
  `update_time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '更新时间',
  `delete_time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '删除时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='用户管理表';

-- ----------------------------
-- Table structure for wait_user_auth
-- ----------------------------
DROP TABLE IF EXISTS `wait_user_auth`;
CREATE TABLE `wait_user_auth` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `user_id` int(10) unsigned NOT NULL COMMENT '用户ID',
  `openid` varchar(32) NOT NULL DEFAULT '' COMMENT 'openid',
  `unionid` varchar(32) NOT NULL DEFAULT '' COMMENT 'unionid',
  `terminal` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '客户端[1=微信小程序, 2=微信公众号, 3=H5, 4=PC, 5=安卓, 6=苹果]',
  `create_time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '创建时间',
  `update_time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='用户授权表';

-- ----------------------------
-- Table structure for wait_user_group
-- ----------------------------
DROP TABLE IF EXISTS `wait_user_group`;
CREATE TABLE `wait_user_group` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  `name` varchar(30) NOT NULL DEFAULT '' COMMENT '名称',
  `remarks` varchar(200) NOT NULL DEFAULT '' COMMENT '备注',
  `sort` smallint(1) unsigned NOT NULL DEFAULT '0' COMMENT '排序',
  `is_delete` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '是否删除: [0=否, 1=是]',
  `create_time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '创建时间',
  `update_time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '更新时间',
  `delete_time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '删除时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='用户分组表';

-- ----------------------------
-- Table structure for wait_user_visitor
-- ----------------------------
DROP TABLE IF EXISTS `wait_user_visitor`;
CREATE TABLE `wait_user_visitor` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  `user_id` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '操作人员',
  `terminal` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '客户端',
  `summary` varchar(100) NOT NULL DEFAULT '' COMMENT '摘要信息',
  `endpoint` varchar(300) NOT NULL DEFAULT '' COMMENT '执行函数',
  `method` varchar(30) NOT NULL DEFAULT '' COMMENT '请求方法',
  `url` varchar(100) NOT NULL DEFAULT '' COMMENT '请求路由',
  `ip` varchar(100) NOT NULL DEFAULT '' COMMENT '请求IP',
  `ua` varchar(300) NOT NULL DEFAULT '' COMMENT '请求UA',
  `user_agent` varchar(900) NOT NULL DEFAULT '' COMMENT 'UA详情',
  `params` text COMMENT '请求参数',
  `error` text COMMENT '错误信息',
  `status` tinyint(1) unsigned NOT NULL DEFAULT '1' COMMENT '执行状态: 1=成功, 2=失败',
  `start_time` varchar(20) NOT NULL DEFAULT '0' COMMENT '开始时间: 毫秒',
  `end_time` varchar(20) NOT NULL DEFAULT '0' COMMENT '结束时间: 毫秒',
  `task_time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '耗时时间: 毫秒',
  `create_time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '操作时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户浏览表';

-- ----------------------------
-- Table structure for wait_user_wallet
-- ----------------------------
DROP TABLE IF EXISTS `wait_user_wallet`;
CREATE TABLE `wait_user_wallet` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `admin_id` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '管理ID',
  `user_id` int(10) unsigned NOT NULL COMMENT '用户ID',
  `log_sn` varchar(64) NOT NULL DEFAULT '' COMMENT '日志编号',
  `action` tinyint(1) unsigned NOT NULL DEFAULT '1' COMMENT '变动类型: [1=增加, 2=减少]',
  `source_sn` varchar(64) NOT NULL DEFAULT '' COMMENT '来源单号',
  `source_id` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '来源主键',
  `source_type` smallint(5) unsigned NOT NULL DEFAULT '0' COMMENT '来源类型',
  `change_amount` decimal(10,2) unsigned NOT NULL DEFAULT '0.00' COMMENT '变动的金额',
  `before_amount` decimal(10,2) unsigned NOT NULL DEFAULT '0.00' COMMENT '变动前数量',
  `after_amount` decimal(10,2) unsigned NOT NULL DEFAULT '0.00' COMMENT '变动后数量',
  `remarks` varchar(200) NOT NULL DEFAULT '' COMMENT '操作的备注',
  `create_time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='用户余额表\n';

-- ----------------------------
-- Insert
-- ----------------------------
BEGIN;
INSERT INTO `wait_auth_admin` VALUES (1, 0, 0, 0, '超级管理员', 'admin', '441c9249be23cb0f884c0d6a08983174', 'zIk6qh', 'static/images/avatar.png', '13800138000', 'admin@qq.com', '127.0.0.1', 1716170400, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_dept` VALUES (1, 0, '陌子科技有限公司', '李墨', '13800138000', 0, 1, '0', 0, 0, 1716170400, 1716170400, 0);
COMMIT;

BEGIN;
INSERT INTO `wait_article_category` VALUES (1, '行业资讯', 0, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_article_category` VALUES (2, '技术分享', 0, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_article` VALUES (1, 1, '0基础学PHP到底有多难', 'static/default/images/article01.jpg', '但是任何一门技术，如果轻易就能够让人学会，那也不会称作为技术，因为那样，工作的可替代性太强了技术，只有难学才会更有价值。对于零基础的同学来说，学习php肯定是非常需要毅力的，任何语言的学习都不可能一蹴而就，而是需要花大量时间，消耗大量精力才能学会的！', '<!DOCTYPE html>\n<html>\n<head>\n</head>\n<body>\n<p>PHP作为WEB端最佳的开发语言，没有华而不实，而是经受住了时间考验，是一门非常值得学习的编程语言。</p>\n<p>目前市场上各种网站、管理系统、小程序、APP等，基本都是使用PHP开发的，也侧面反映了PHP的需求以及学习的必要性！</p>\n<p>对于刚接触PHP的同学，作为过来人，这里分享一下PHP的一些学习经验！</p>\n<p>&nbsp;</p>\n<p><strong>一、学php难吗？</strong></p>\n<p>难！</p>\n<p>但是任何一门技术，如果轻易就能够让人学会，那也不会称作为技术，因为那样，工作的可替代性太强了技术，只有难学才会更有价值。对于零基础的同学来说，学习php肯定是非常需要毅力的，任何语言的学习都不可能一蹴而就，而是需要花大量时间，消耗大量精力才能学会的！</p>\n<p>&nbsp;</p>\n<p><strong>二、学php有没有技巧？</strong></p>\n<p>当然有，这也是这篇文章想说明的</p>\n<p>&nbsp;</p>\n<ul>\n<li>\n<p><strong>php学习第一要点：心态</strong></p>\n</li>\n</ul>\n<p>虽然目前php语言市场火爆，而且php语言相对于其他语言来说也更容易学习，但是千万别把php想的太简单，不要全信培训学校的宣传，仿佛零基础的人分分钟钟，随随便便就将php学会。</p>\n<p>失败的案例肯定不少。</p>\n<p>当然我也不要把php想的太难，既然你想从事这方面的工作，那么就要准备全力以赴，破釜沉舟。3个月学会不会，那就坚持到4个月，4个月还不会，那就坚持到5个月（需要一点点乌龟精神），总有一天，会全面掌握php知识，拿到自己满意的薪酬。</p>\n<p>&nbsp;</p>\n<ul>\n<li>\n<p><strong>php学习的第二要点：就是学习方法</strong></p>\n</li>\n</ul>\n<p>这里，建议大家还是报一个班，比如php中文网，他们家也有线上直播班，口碑一直不错。</p>\n<p>一个人学习php太难，如果说有一群人一起来学习，就能够营造出一种学习php氛围，有老师教，学习php碰到问题也可以得到解决。</p>\n<p>这里，就会碰到一个问题，那就是一个班，有零基础的、有从事过这方面工作的，php水平可谓是层次不齐，如果是一个零基础的同学学习php，如何跟上学校的讲课进度？</p>\n<p>&nbsp;</p>\n<ul>\n<li>\n<p><strong>php学习的第三要点：那就是坚持、坚持、再坚持，抵御诱惑</strong></p>\n</li>\n</ul>\n<p>PHP是最适合新手入门学习的首选语言，但是很多新手刚接触编程无所适从，也许学了一半PHP，又开始打C#主意，或者有人说JA VA 很强，这个时候的绝对不能动摇，哪怕我真想学，也得学会了PHP然后再学。</p>\n<p>见异思迁，是最不可取的！狗熊掰玉米就是这个道理，如果经常中途放弃，只能是一无所获，还浪费了N多的时间和经历。当我花费了大量精力后却又放弃了php，相信心里面会很难过，对未来又会陷入到迷茫中，严重打击自信心。</p>\n<p>&nbsp;</p>\n<p><strong>三、如果不想有这种体验，那就坚持学会php吧！</strong></p>\n</body>\n</html>', 0, 0, 0, 1, 1, 1, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_article` VALUES (2, 1, '28岁了打算入行PHP还来得及吗', 'static/default/images/article02.jpg', '来不来得及不用考虑，只要你技术学的扎实，找一份工作还是没问题。你要考虑的是转行成本：如果你现在只是拿着四五千的薪资，工作也没什么成长性，即使辞了这份工作，很容易也能找到差不多的，那你可以考虑入行PHP。', '<!DOCTYPE html>\n<html>\n<head>\n</head>\n<body>\n<p>来不来得及不用考虑，只要你技术学的扎实，找一份工作还是没问题。</p>\n<p><strong>你要考虑的是转行成本：</strong></p>\n<p>如果你现在只是拿着五六千的薪资，工作也没什么成长性，即使辞了这份工作，很容易也能找到差不多的，那你可以考虑入行PHP。</p>\n<p>虽然没有年龄上的优势，但是同样的，你在28岁这个年纪，就算转入任何一个行业皆是如此。</p>\n<p>就看你自己有没有破釜沉舟的决心，以及能不能抗住学习的压力和刚进公司的压力。</p>\n<p><strong>至少在目前迈进PHP行业的门槛并不高：</strong></p>\n<p>1、会一些简单的&nbsp;<code>HTML+CSS+JavaScript&nbsp;</code>就可以完成简单的页面布局；</p>\n<p>2、掌握基本的<code>PHP+MySQL</code>，学习如何将<code>PHP</code>与<code>前端</code>结合起来，完成简单的动态页面。</p>\n<p>3、学习一些主流前后端框架，比如<code>ThinkPHP</code>、<code>LayUI</code>，提升开发效率， 最终完成一个功能齐全的动态站点。</p>\n<p>&nbsp;</p>\n<p>另外这个行业并不是只能一开始就来，后来的都上不了车，不像医生，老师，律师，金融等行业一样，把车门都给你焊的死死的。</p>\n<p>&nbsp;</p>\n<p><strong>只要肯努力，多做项目，多学习，一年肯定能称得上别人三年的经验，成为 &ldquo; 后起之秀 &rdquo;！</strong></p>\n<p><strong>加油！</strong></p>\n</body>\n</html>', 0, 0, 0, 1, 1, 1, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_article` VALUES (3, 1, '初中级的PHPer应该具备这些技能', 'static/default/images/article03.jpg', '又到了，金三银四，换工作季。我没准备换工作，倒是上网翻了翻招聘信息，由于我做PHP，就看了下当下3-5年的招聘需求，发现这些招聘信息都有如下要求', '<!DOCTYPE html>\n<html>\n<head>\n</head>\n<body>\n<p><strong>3-5年PHP需要具备：</strong></p>\n<ul>\n<li><code>TCP/UDP</code>协议，&nbsp;<code>socket</code>通信，熟练使用<code>workman</code>，<code>swoole</code>，<code>swoft</code>等rpc框架</li>\n<li>精通<code>PHP</code>，另外最好熟悉一门其他编程语言</li>\n<li>熟悉<code>html</code>，<code>css</code>，<code>javascript</code>，会<code>nodejs</code>，<code>vue</code>优先</li>\n<li><code>mysql</code>， 以及<code>SQL</code>优化，熟悉索引应用和优化，独立设计数据库、数据表</li>\n<li><code>nosql</code>，<code>mongodb</code>，&nbsp;<code>redis</code>，<code>memcache</code>缓存。熟悉后端缓存技术、了解缓存使用场景，高并发、高性能服务系统设计经验及能力，熟悉大规模集群系统的开发</li>\n<li>常用<code>Linux</code>，<code>shell</code>命令编写，熟悉云、容器使用</li>\n<li>精通<code>LNMP</code>架构，熟悉<code>http&nbsp;</code>协议，<code>RestFul API</code>开发，熟悉<code>tp</code>，<code>laravel</code>，<code>yii</code>主流框架。</li>\n<li>熟练使用<code>svn</code>，<code>git</code>，<code>Hg</code>版本管理工具，</li>\n<li>良好的书写习惯，注释，设计模式，编写高质量的，整洁简单，可维护性的代码，遵循公司研发规范，产品技术文档的整理</li>\n<li>分析和快速排查定位解决线上问题，保障系统功能的稳定性，优化现有系统，提升运作性能</li>\n<li>主导/参与项目的架构设计、技术选型、架构原型实现以及服务端核心模块的开发，与各技术人员紧密合作，完成工作任务</li>\n<li>有个人博客，个人开源项目，有个人独立完成项目。</li>\n<li>乐于持续学习，乐观开朗，抗压性强，良好的沟通能力和合作精神，自我驱动力强，有强烈的事业心和责任感</li>\n</ul>\n<p>大家可以看看自己是否达到了主流的用人标准，如果你是超出预期，那么你可以选择跳得更高。</p>\n<p>3-5年时间，足够把一个学生培养成一个合格的打工人了。可以看到企业还是把PHPer当作多面手看待，希望不仅需要精通PHP，还需要掌握前端和运维等方面的知识。对技术高低的评判主要是对高性能、高并发的设计，这个时候会不会用第三方工具（Redis，ES），了不了解限流、队列、削峰、缓存这些原理就尤为重要。</p>\n<p>3-5年的phper，企业还希望有一定的带团能力，由此可见phper的成熟期是较短的。</p>\n<p>我同时对比了3-5年的NodeJS，Python、Java、Golang就职要求，要求本科以上，至少4年以上经验，更侧重逻辑算法，门槛比较高。</p>\n<p>或许去年疫情情况，让很多人觉得PHP岗位是不是少了，其实疫情对于IT公司多少都有所影响，各个技术岗位裁员也是难免的，不过这些只是短暂的变动。</p>\n</body>\n</html>', 0, 0, 0, 1, 1, 1, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_article` VALUES (4, 1, '别再学这五个要被淘汰的编程语言了', 'static/default/images/article04.jpg', '编程语言都有自己的生命周期，对某些语言来说，属于它们的时代似乎已经结束了，今天，我们就来盘下一下目前前景最黯淡的5种语言。', '<!DOCTYPE html>\n<html>\n<head>\n</head>\n<body>\n<p>每个编码的人都有自己喜欢的语言。拥有一种首选语言有很多原因，但是，我们的语言有时会变得很单调，它不再由制造它的公司维护，或者人们出于某种无法解释的原因放弃使用它。但是，也有的编程语言例外，比如C语言，它就经受住了时间的考验，在许多情况下仍然是最流行的编程语言。</p>\n<p>编程语言都有自己的生命周期，对某些语言来说，属于它们的时代似乎已经结束了，今天，我们就来盘下一下目前前景最黯淡的5种语言：</p>\n<p>&nbsp;</p>\n<p><strong>1. Visual Basic .NET</strong></p>\n<p>Microsoft Visual Basic.NET 是 Microsoft Visual Basic 6.0 的后续版本，它是基于 .NET 框架重新设计的，在1991年，微软增强了BASIC语言，将其包含到语言中，形成了Visual Basic，后来发生了一些事情：德尔福（Borland）的负责人安德斯&middot;海尔斯伯格（Anders Hejlsberg）离开了公司，加入了微软，在那里他开始了C#项目。</p>\n<p>这种语言在许多方面与Java相似，一段时间后，C#成为了微软的新语言标准。与c#诞生同时，微软程序员发明了VisualBasic . net，它的语法与BASIC相同，但代码模仿了C#。这两种语言都广为人知，但c#似乎赢得了流行度的竞赛。因此，Visual Basic似乎注定要消亡。</p>\n<p>&nbsp;</p>\n<p><strong>2.Delphi</strong></p>\n<p>Delphi，也就是Pascal + Objects，最有可能被淘汰，即便Embarcadero已经尝试支持它，新版本仍在发布中。这主要归结于Borland的一系列战略失误。</p>\n<p>首先，，他们把名字改成了Imprise。然而，这并没有起作用，于是又回到了之前的名字，并突然将他们的数据库工具从编程工具中分离出来。</p>\n<p>后者被重新命名为CodeGear，但出于某种原因，人们开始怀疑出了什么问题：如此频繁的名称更改，如此频繁的战略更改，让这门语言的拥护者离他而去。</p>\n<p>Embarcadero的持续努力是否能让Delphi继续下去还有待观察，但很明显Delphi在编程世界中正在失去青睐。也许是时候换一个不同的平台了。</p>\n<p>&nbsp;</p>\n<p><strong>3.Perl</strong></p>\n<p>曾经有一段时间，每个人都用Perl编程，但是后来发生了一些事情，开发者开始在不知道原因的情况下添加越来越大的功能，也许这增加了了问题的复杂性。甚至它的作者似乎已经含蓄地解释了Perl的一些问题，并选择停止从2000年开始的Perl 6开发，关键是，似乎现在也没人想要在用Perl。</p>\n<p>&nbsp;</p>\n<p><strong>4. Adobe Flash</strong></p>\n<p>我们这里讨论的不是语言，而是平台。当史蒂夫&middot;乔布斯选择不在苹果的移动设备上使用Adobe Flash时，Adobe Flash的丧钟就敲响了。</p>\n<p>如果其中一个新平台，比如苹果的平板电脑，不支持Flash应用程序，开发者将不得不使用Javascript、HTML5或其他苹果批准的平台来创建这些应用程序。结果，Flash尽管不断进步，却开始衰落。如今，它还是避免不了消亡。</p>\n<p>&nbsp;</p>\n<p><strong>5.Ruby</strong></p>\n<p>Ruby在大约10年前风靡一时，它在1995年首次亮相后就有了一大批的拥护者，很多人会拿Ruby和C类语言做比较。</p>\n<p>毫无疑问，这是一种非常棒的编程语言，尽管它的发展速度很慢，例如，Twitter有许多用Ruby构建的东西，但由于效率低下而放弃了它，而这一发现的那天很可能就是Ruby开始消亡的那天。</p>\n</body>\n</html>', 0, 0, 0, 1, 1, 1, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_article` VALUES (5, 2, '怎么用php实现多对一通讯录', 'static/default/images/article05.jpg', '随着移动互联网的快速发展，人们使用手机和电脑联系和交流的方式已经越来越多样化。电话、邮件、短信、社交媒体应用等，使得人们可以从各种角度与朋友、家人、同事等联系。', '<!DOCTYPE html>\n<html>\n<head>\n</head>\n<body>\n<p>随着移动互联网的快速发展，人们使用手机和电脑联系和交流的方式已经越来越多样化。电话、邮件、短信、社交媒体应用等，使得人们可以从各种角度与朋友、家人、同事等联系。然而，这些手段有时解决不了一些需要快速协作和沟通的问题，比如企业内部联系人的管理、学校老师和学生之间的通讯录共享等。这时，多对一的通讯录就成为了必需品。本文将介绍如何利用PHP语言实现多对一的通讯录功能。</p>\n<p>&nbsp;</p>\n<p><strong>一. 通讯录的基本功能</strong></p>\n<ul>\n<li>\n<p>添加联系人：包括联系人的姓名、电话、邮箱、公司、职位等基本信息。</p>\n</li>\n<li>\n<p>编辑联系人：对已有联系人的信息进行修改。</p>\n</li>\n<li>\n<p>删除联系人：删除已有联系人的信息。</p>\n</li>\n<li>\n<p>按条件查找联系人：可以通过关键字或者类别等方式来查找已有的联系人。</p>\n</li>\n<li>\n<p>导出联系人：将通讯录的联系人信息导出为Excel或CSV格式存储在电脑或手机上供离线使用。</p>\n</li>\n<li>\n<p>备份通讯录：定期备份通讯录的联系人信息，防止数据丢失。</p>\n</li>\n</ul>\n<p>&nbsp;</p>\n<p><strong>二. 多对一通讯录的设计思路</strong></p>\n<p>在多对一的通讯录中，多个用户共享同一个通讯录的数据。为了保证数据的安全性和用户能够顺利访问通讯录，需要进行以下设计：</p>\n<ul>\n<li>\n<p>数据库的设计：利用关系型数据库存储通讯录的联系人信息并进行数据权限控制，防止未经授权的人员访问通讯录。</p>\n</li>\n<li>\n<p>用户认证：为了保证对通讯录的访问权限，需要在应用中添加用户认证功能。</p>\n</li>\n<li>\n<p>用户管理：建立一个用户管理界面，可以对用户的权限进行管理，以及对用户进行添加、修改和删除等操作。</p>\n</li>\n<li>\n<p>数据展示：从数据库中提取通讯录信息显示在页面上。可以通过搜索、分类、排序等方式实现通讯录中的信息管理。</p>\n</li>\n<li>\n<p>权限控制：根据不同用户的权限，控制用户可以看到的通讯录信息。</p>\n</li>\n</ul>\n<p>&nbsp;</p>\n<p><strong>三. 实现多对一通讯录的具体步骤</strong></p>\n<p>以下是实现多对一通讯录的具体步骤：</p>\n<ul>\n<li>\n<p>创建数据库并建立适当的表结构，包括用户表和联系人表等。</p>\n</li>\n<li>\n<p>开发用户认证功能和用户管理功能，采用常见的用户认证方式，比如用户名和密码认证等。</p>\n</li>\n<li>\n<p>开发联系人的添加、编辑和删除功能，并实现数据的有效性验证和存储。</p>\n</li>\n<li>\n<p>实现通讯录的筛选、排序、分类等功能。可以采用Ajax技术，提高用户体验。</p>\n</li>\n<li>\n<p>开发导出联系人和备份通讯录的功能。可以通过第三方软件或类库实现。</p>\n</li>\n<li>\n<p>实现权限控制功能，根据用户的权限将数据进行展示。</p>\n</li>\n</ul>\n<p>&nbsp;</p>\n<p><strong>四. 总结</strong></p>\n<p>本文介绍了如何利用PHP语言实现多对一的通讯录功能。一个好的通讯录应当具有方便、实用、安全等特点，更好的实现信息管理的需要。本文提供了一些设计思路和实现步骤，希望能够为PHP开发者提供帮助和启示。要想实现一个完整的多对一通讯录功能，还需要不断地学习和研究相关技术和工具，提高自己的编程能力和实践经验。</p>\n</body>\n</html>', 0, 0, 0, 1, 1, 1, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_article` VALUES (6, 2, 'PHP如何实现不模糊包含表达式', 'static/default/images/article06.jpg', '不模糊包含表达式是指匹配字符串时必须完全匹配，而不是只匹配部分字符。在 PHP 中，可以使用 preg_match 函数来实现正则表达式匹配。', '<!DOCTYPE html>\n<html>\n<head>\n</head>\n<body>\n<p>不模糊包含表达式是指匹配字符串时必须完全匹配，而不是只匹配部分字符。在 PHP 中，可以使用 preg_match 函数来实现正则表达式匹配。</p>\n<p>&nbsp;</p>\n<p>例如，假设需要匹配的字符串为 \"hello world\"，则可以使用如下正则表达式：</p>\n<pre class=\"language-php\"><code>/^hello world$/</code></pre>\n<p>其中，^ 表示匹配字符串开头，$ 表示匹配字符串结尾。这样就可以确保只匹配完全相同的字符串，而不会模糊包含。</p>\n</body>\n</html>', 0, 0, 0, 1, 1, 1, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_article` VALUES (7, 2, 'PHP中Linux文件路径是否存在怎么判断?', 'static/default/images/article07.jpg', 'php linux文件路径是否存在的判断方法：1、使用linux命令“[ -f qipa250.txt ] && echo yes || echo no”判断文件是否存在；2、通过php调用linux命令，代码是“$pdf_file_exists = \'[ -f \' . $pdf_file_url . \' ] && echo true || echo false\';”', '<!DOCTYPE html>\n<html>\n<head>\n</head>\n<body>\n<blockquote>\n<p>php linux文件路径是否存在的判断方法：1、使用linux命令&ldquo;[ -f qipa250.txt ] &amp;&amp; echo yes || echo no&rdquo;判断文件是否存在；2、通过php调用linux命令，代码是&ldquo;$pdf_file_exists = \'[ -f \' . $pdf_file_url . \' ] &amp;&amp; echo true || echo false\';&rdquo;</p>\n</blockquote>\n<p>&nbsp;</p>\n<p>本教程操作环境：linux5.9.8系统、PHP8.1、Dell G3电脑。</p>\n<p><strong>php使用linux命令判断文件是否存在</strong></p>\n<p>Linux一句命令之判断文件是否存在</p>\n<pre class=\"language-php\"><code>[ -f qipa250.txt ] &amp;&amp; echo yes || echo no</code></pre>\n<p>-f 文件名字文件存在则为真。</p>\n<p>执行[ -f qipa250.txt ]为真则执行echo yes，由于或语句||的存在echo no不再执行。</p>\n<p>特别注意的是，这里的逻辑与和逻辑或值得仔细思考。</p>\n<p>php调用linux命令方法</p>\n<pre class=\"language-php\"><code>//指定文件路径\n\n$pdf_file_url=\'/data/web/QipaFile/qipa250.pdf\';\n\n//命令\n\n$pdf_file_exists = \'[ -f \' . $pdf_file_url . \' ] &amp;&amp; echo true || echo false\';\n\n//执行\n\necho $pdf_file_exists_result = system($pdf_file_exists);</code></pre>\n<p>&nbsp;</p>\n</body>\n</html>', 0, 0, 0, 1, 1, 1, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_article` VALUES (8, 2, 'PHP中多态性是什么意思?', 'static/default/images/article08.jpg', '在PHP中，多态性是指同一个操作作用于不同的类的实例，将产生不同的执行结果。也即不同类的对象收到相同的消息时，将得到不同的结果；不同的对象，收到同一消息将可以产生不同的结果，这种现象称为多态性。多态性允许每个对象以适合自身的方式去响应共同的消息；多态性增强了软件的灵活性和重用性。', '<!DOCTYPE html>\n<html>\n<head>\n</head>\n<body>\n<blockquote>\n<p>在PHP中，多态性是指同一个操作作用于不同的类的实例，将产生不同的执行结果。也即不同类的对象收到相同的消息时，将得到不同的结果；不同的对象，收到同一消息将可以产生不同的结果，这种现象称为多态性。多态性允许每个对象以适合自身的方式去响应共同的消息；多态性增强了软件的灵活性和重用性。</p>\n</blockquote>\n<p>&nbsp;</p>\n<h2><strong>PHP 多态性</strong></h2>\n<p>多态性是指相同的操作或函数、过程可作用于多种类型的对象上并获得不同的结果。不同的对象，收到同一消息将可以产生不同的结果，这种现象称为多态性。</p>\n<p>多态性允许每个对象以适合自身的方式去响应共同的消息。多态性增强了软件的灵活性和重用性。</p>\n<p>在面向对象的软件开发中，多态性是最为重要的部分之一。面向对象编程并不只是将相关的方法与数据简单的结合起来，而是采用面向对象编程中的各种要素将现实生活中的各种情况清晰的描述出来。这一小节将对面向对象编程中的多态性作详细的讲解。</p>\n<p>&nbsp;</p>\n<p><strong>1.什么是多态</strong></p>\n<p>多 态（Polymorphism）按字面上意思理解就是&ldquo;多种形状&rdquo;。可以理解为多种表现形式，也即&ldquo;一个对外接口，多个内部实现方法&rdquo;。在面向对象的理论 中，多态性的一般定义为：同一个操作作用于不同的类的实例，将产生不同的执行结果。也即不同类的对象收到相同的消息时，将得到不同的结果。</p>\n<p>在实际的应用开发中，采用面向对象中的多态主要在于可以将不同的子类对象都当作一个父类来处理，并且可以屏蔽不同子类对象之间所存在的差异，写出通用的代码，做出通用的编程，以适应需求的不断变化。</p>\n<p>&nbsp;</p>\n<p><strong>2. 多态的应用设计</strong></p>\n<p>在实际的应用开发中，通常为了使项目能够在以后的时间里的轻松实现扩展与升级，需要通过继承实现可复用模块进行轻松升级。在进行可复用模块设计时，就需要尽可能的减少使用流程控制语句。此时就可以采用多态实现该类设计。</p>\n</body>\n</html>', 0, 0, 0, 0, 1, 1, 0, 1716170400, 1716170400, 0);
COMMIT;

BEGIN;
INSERT INTO `wait_dev_banner` VALUES (1, 10, '别再学这五个被淘汰的语言了', 'static/default/images/banner01.webp', '_blank', '/article/detail/4', 0, 0, 0, 1721272137, 1721272137, 0);
INSERT INTO `wait_dev_banner` VALUES (2, 10, 'WaitAdmin开源快速开发框架', 'static/default/images/banner02.webp', '_blank', 'https://gitee.com/wafts/WaitAdmin', 0, 0, 0, 1721272200, 1721272200, 0);
INSERT INTO `wait_dev_banner` VALUES (3, 20, '阿里云特惠服务器推荐', 'static/default/images/adv01.jpg', '_blank', 'https://www.aliyun.com/minisite/goods?userCode=m5k1mahd&share_source=copy_link', 0, 0, 0, 1679073786, 1679124684, 0);
INSERT INTO `wait_dev_banner` VALUES (4, 20, 'WaitShop开源电商系统', 'static/default/images/adv02.jpg', '_blank', 'https://gitee.com/wafts/WaitShop', 0, 0, 0, 1679073793, 1679124639, 0);
COMMIT;

BEGIN;
INSERT INTO `wait_dev_links` VALUES (1, 'Layui', '', '_blank', 'https://layui.github.io/', 0, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_dev_links` VALUES (2, 'ThinkPHP', '', '_blank', 'https://www.thinkphp.cn/', 0, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_dev_links` VALUES (3, 'WaitAdmin', '', '_blank', 'https://www.waitadmin.cn/', 0, 0, 0, 1716170400, 1716170400, 0);
COMMIT;

BEGIN;
INSERT INTO `wait_notice_setting` VALUES (1, 101, '短信免密登录', '手机短信登录时发送', '{\"code\":\"验证码\"}', '{}', '{\"status\":\"1\",\"content\":\"您的验证码：${code}，您正进行身份验证，打死不告诉别人！\",\"template_code\":\"SMS_182535543\"}', '{}', 1, 1, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_notice_setting` VALUES (2, 102, '找回登录密码', '找回登录密码时发送', '{\"code\":\"验证码\"}', '{}', '{\"status\":\"1\",\"content\":\"您的验证码：${code}，您正进行身份验证，打死不告诉别人！\",\"template_code\":\"SMS_182535543\"}', '{}', 1, 1, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_notice_setting` VALUES (3, 103, '手机注册账号', '手机注册账号时发送', '{\"code\":\"验证码\"}', '{}', '{\"status\":\"1\",\"content\":\"您的验证码：${code}，您正进行身份验证，打死不告诉别人！\",\"template_code\":\"SMS_182535543\"}', '{}', 1, 1, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_notice_setting` VALUES (4, 104, '手机号码绑定', '手机账号绑定时发送', '{\"code\":\"验证码\"}', '{}', '{\"status\":\"1\",\"content\":\"您的验证码：${code}，您正进行身份验证，打死不告诉别人！\",\"template_code\":\"SMS_182535543\"}', '{}', 1, 1, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_notice_setting` VALUES (5, 105, '手机号码变更', '手机号码变更时发送', '{\"code\":\"验证码\"}', '{}', '{\"status\": \"1\", \"content\": \"\\u60a8\\u6b63\\u5728\\u53d8\\u66f4\\u624b\\u673a\\u53f7\\uff0c\\u9a8c\\u8bc1\\u7801${code}\\uff0c\\u5207\\u52ff\\u5c06\\u9a8c\\u8bc1\\u7801\\u6cc4\\u9732\\u4e8e\\u4ed6\\u4eba\\uff0c\\u672c\\u6761\\u9a8c\\u8bc1\\u7801\\u6709\\u6548\\u671f5\\u5206\\u949f\\u3002\", \"template_code\": \"SMS_207952628\"}', '{}', 1, 1, 0, 1716170400, 1721187495, 0);
INSERT INTO `wait_notice_setting` VALUES (6, 106, '邮箱注册账号', '邮箱注册账号时发送', '{\"code\":\"验证码\"}', '{}', '{}', '{\"status\": \"1\", \"content\": \"\\u60a8\\u7684\\u9a8c\\u8bc1\\u7801\\uff1a${code}\\uff0c\\u60a8\\u6b63\\u8fdb\\u884c\\u8eab\\u4efd\\u9a8c\\u8bc1\\uff0c\\u6253\\u6b7b\\u4e0d\\u544a\\u8bc9\\u522b\\u4eba\\uff01\"}', 1, 1, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_notice_setting` VALUES (7, 107, '邮箱账号绑定', '邮箱账号绑定时发送', '{\"code\":\"验证码\"}', '{}', '{}', '{\"status\": \"1\", \"content\": \"\\u60a8\\u7684\\u9a8c\\u8bc1\\u7801\\uff1a${code}\\uff0c\\u60a8\\u6b63\\u8fdb\\u884c\\u8eab\\u4efd\\u9a8c\\u8bc1\\uff0c\\u6253\\u6b7b\\u4e0d\\u544a\\u8bc9\\u522b\\u4eba\\uff01\"}', 1, 1, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_notice_setting` VALUES (8, 108, '邮箱账号变更', '邮箱账号变更时发送', '{\"code\":\"验证码\"}', '{}', '{}', '{\"status\": \"1\", \"content\": \"\\u60a8\\u7684\\u9a8c\\u8bc1\\u7801\\uff1a${code}\\uff0c\\u60a8\\u6b63\\u8fdb\\u884c\\u8eab\\u4efd\\u9a8c\\u8bc1\\uff0c\\u6253\\u6b7b\\u4e0d\\u544a\\u8bc9\\u522b\\u4eba\\uff01\"}', 1, 1, 0, 1716170400, 1716170400, 0);
COMMIT;

BEGIN;
INSERT INTO `wait_dev_pay_config` VALUES (2, 2, '微信支付', '微信支付', 'static/images/pay_z_wxpay.png', 'static/images/pay_wxpay.png', '{\"merchant_type\": \"ordinary_merchant\", \"interface_version\": \"v3\", \"mch_id\": \"\", \"secret_key\": \"\", \"apiclient_cert\": \"\", \"apiclient_key\": \"\"}', 3, 1, 1716170400, 1716170400);
INSERT INTO `wait_dev_pay_config` VALUES (3, 3, '支付宝支付', '支付宝支付', 'static/images/pay_z_alipay.png', 'static/images/pay_alipay.png', '{\"merchant_type\": \"ordinary_merchant\", \"app_id\": \"\", \"private_key\": \"\", \"public_key\": \"\"}', 2, 1, 1716170400, 1716170400);
COMMIT;

BEGIN;
INSERT INTO `wait_sys_config` VALUES (10, 'backs', 'name', 'WaitAdmin(python)管理系统', '', 1716170400, 1716170400);
INSERT INTO `wait_sys_config` VALUES (11, 'backs', 'title', 'WaitAdmin(python)管理系统', '', 1716170400, 1716170400);
INSERT INTO `wait_sys_config` VALUES (12, 'backs', 'cover', '', '', 1716170400, 1716170400);
INSERT INTO `wait_sys_config` VALUES (13, 'backs', 'favicon', 'static/images/favicon.ico', '', 1716170400, 1716170400);
INSERT INTO `wait_sys_config` VALUES (14, 'backs', 'logo_black_big', 'static/images/logo_black_big.png', '', 1716170400, 1716170400);
INSERT INTO `wait_sys_config` VALUES (15, 'backs', 'logo_black_small', 'static/images/logo_black_small.png', '', 1716170400, 1716170400);
INSERT INTO `wait_sys_config` VALUES (16, 'backs', 'logo_white_big', 'static/images/logo_white_big.png', '', 1716170400, 1716170400);
INSERT INTO `wait_sys_config` VALUES (17, 'backs', 'logo_white_small', 'static/images/logo_white_small.png', '', 1716170400, 1716170400);
INSERT INTO `wait_sys_config` VALUES (18, 'backs', 'contacts', '李零', '', 1716170400, 1716170400);
INSERT INTO `wait_sys_config` VALUES (19, 'backs', 'mobile', '13800138000', '', 1716170400, 1716170400);
INSERT INTO `wait_sys_config` VALUES (110, 'website', 'icp', '粤ICP备0000000号', '', 1716170400, 1716170400);
INSERT INTO `wait_sys_config` VALUES (111, 'website', 'pcp', '粤公网安备 28888880000000号', '', 1716170400, 1716170400);
INSERT INTO `wait_sys_config` VALUES (112, 'website', 'copyright', '© 2023-2024 WaitAdmin开源团队工作室 版权所有 · www.waitadmin.cn', '', 1716170400, 1716170400);
INSERT INTO `wait_sys_config` VALUES (113, 'website', 'analyse', '', '', 1716170400, 1716170400);
INSERT INTO `wait_sys_config` VALUES (140, 'h5', 'logo', '', '', 1716170400, 1716170400);
INSERT INTO `wait_sys_config` VALUES (141, 'h5', 'title', '', '', 1716170400, 1716170400);
INSERT INTO `wait_sys_config` VALUES (142, 'h5', 'status', '1', '', 1716170400, 1716170400);
INSERT INTO `wait_sys_config` VALUES (143, 'h5', 'close_url', '', '', 1716170400, 1716170400);
INSERT INTO `wait_sys_config` VALUES (170, 'pc', 'favicon', 'static/images/favicon.ico', '', 1716170400, 1716170400);
INSERT INTO `wait_sys_config` VALUES (171, 'pc', 'logo', 'static/images/logo_pc.png', '', 1716170400, 1716170400);
INSERT INTO `wait_sys_config` VALUES (172, 'pc', 'name', 'WaitAdmin(Python)开源管理系统', '', 1716170400, 1716170400);
INSERT INTO `wait_sys_config` VALUES (173, 'pc', 'title', 'WaitAdmin(Python)开源管理系统', '', 1716170400, 1716170400);
INSERT INTO `wait_sys_config` VALUES (174, 'pc', 'keywords', 'python通用后台,fastapi后台管理系统,vue3后台管理系统,cms管理系统', '', 1716170400, 1716170400);
INSERT INTO `wait_sys_config` VALUES (175, 'pc', 'description', 'WaitAdmin(python)Fastapi+Vue3开发的一套快速开发通用管理后台，集成Vue常用组件，RBAC权限管理， 让开发变的简单，界面简洁清爽，后台支持多种菜单结构可满足不同人群的需求，非常适合二开做项目。', '', 1716170400, 1716170400);
INSERT INTO `wait_sys_config` VALUES (210, 'policy', 'service', '', '', 1716170400, 1716170400);
INSERT INTO `wait_sys_config` VALUES (211, 'policy', 'privacy', '', '', 1716170400, 1716170400);
INSERT INTO `wait_sys_config` VALUES (212, 'policy', 'payment', '', '', 1716170400, 1716170400);
INSERT INTO `wait_sys_config` VALUES (310, 'login', 'is_agreement', '1', '', 1716170400, 1716170400);
INSERT INTO `wait_sys_config` VALUES (311, 'login', 'defaults', 'account', '', 1716170400, 1716170400);
INSERT INTO `wait_sys_config` VALUES (312, 'login', 'registers', '[\"mobile\"]', '', 1716170400, 1716170400);
INSERT INTO `wait_sys_config` VALUES (313, 'login', 'login_modes', '[\"account\"]', '', 1716170400, 1716170400);
INSERT INTO `wait_sys_config` VALUES (314, 'login', 'login_other', '[\"wx\"]', '', 1716170400, 1716170400);
INSERT INTO `wait_sys_config` VALUES (410, 'storage', 'engine', 'local', '', 1716170400, 1716170400);
INSERT INTO `wait_sys_config` VALUES (411, 'storage', 'qiniu', '{\"bucket\": \"\", \"domain\": \"\", \"access_key\": \"\", \"secret_key\": \"\", \"region\": \"\"}', '', 1716170400, 1716170400);
INSERT INTO `wait_sys_config` VALUES (412, 'storage', 'aliyun', '{\"bucket\": \"\", \"domain\": \"\", \"access_key\": \"\", \"secret_key\": \"\", \"region\": \"\"}', '', 1716170400, 1716170400);
INSERT INTO `wait_sys_config` VALUES (413, 'storage', 'qcloud', '{\"bucket\": \"\", \"domain\": \"\", \"access_key\": \"\", \"secret_key\": \"\", \"region\": \"\"}', '', 1716170400, 1716170400);
INSERT INTO `wait_sys_config` VALUES (510, 'sms', 'aliyun', '{\"sign\": \"\", \"app_id\": \"\", \"acc_key\": \"\", \"acc_secret\": \"\"}', '', 1716170400, 1716170400);
INSERT INTO `wait_sys_config` VALUES (511, 'sms', 'engine', 'tencent', '', 1716170400, 1716170400);
INSERT INTO `wait_sys_config` VALUES (512, 'sms', 'tencent', '{\"sign\": \"\", \"app_id\": \"\", \"acc_key\": \"\", \"acc_secret\": \"\"}', '', 1716170400, 1716170400);
INSERT INTO `wait_sys_config` VALUES (610, 'email', 'smtp_type', 'smtp', '', 1716170400, 1716170400);
INSERT INTO `wait_sys_config` VALUES (611, 'email', 'smtp_host', '', '', 1716170400, 1716170400);
INSERT INTO `wait_sys_config` VALUES (612, 'email', 'smtp_port', '', '', 1716170400, 1716170400);
INSERT INTO `wait_sys_config` VALUES (613, 'email', 'smtp_user', '', '', 1716170400, 1716170400);
INSERT INTO `wait_sys_config` VALUES (614, 'email', 'smtp_pass', '', '', 1716170400, 1716170400);
INSERT INTO `wait_sys_config` VALUES (615, 'email', 'verify_type', 'default', '', 1716170400, 1716170400);
INSERT INTO `wait_sys_config` VALUES (710, 'wx_channel', 'name', '', '', 1716170400, 1716170400);
INSERT INTO `wait_sys_config` VALUES (711, 'wx_channel', 'original_id', '', '', 1716170400, 1716170400);
INSERT INTO `wait_sys_config` VALUES (712, 'wx_channel', 'qr_code', '', '', 1716170400, 1716170400);
INSERT INTO `wait_sys_config` VALUES (713, 'wx_channel', 'app_id', '', '', 1716170400, 1716170400);
INSERT INTO `wait_sys_config` VALUES (714, 'wx_channel', 'app_secret', '', '', 1716170400, 1716170400);
INSERT INTO `wait_sys_config` VALUES (730, 'oa_channel', 'name', '', '', 1716170400, 1716170400);
INSERT INTO `wait_sys_config` VALUES (731, 'oa_channel', 'original_id', '', '', 1716170400, 1716170400);
INSERT INTO `wait_sys_config` VALUES (732, 'oa_channel', 'qr_code', '', '', 1716170400, 1716170400);
INSERT INTO `wait_sys_config` VALUES (733, 'oa_channel', 'app_id', '', '', 1716170400, 1716170400);
INSERT INTO `wait_sys_config` VALUES (734, 'oa_channel', 'app_secret', '', '', 1716170400, 1716170400);
INSERT INTO `wait_sys_config` VALUES (735, 'oa_channel', 'token', '', '', 1716170400, 1716170400);
INSERT INTO `wait_sys_config` VALUES (736, 'oa_channel', 'aes_key', '', '', 1716170400, 1716170400);
INSERT INTO `wait_sys_config` VALUES (737, 'oa_channel', 'encryption_type', '1', '', 1716170400, 1716170400);
INSERT INTO `wait_sys_config` VALUES (750, 'op_channel', 'app_id', '', '', 1716170400, 1716170400);
INSERT INTO `wait_sys_config` VALUES (751, 'op_channel', 'app_secret', '', '', 1716170400, 1716170400);
COMMIT;

BEGIN;
INSERT INTO `wait_auth_menu` VALUES (1, 0, 'C', '首页', 'el-icon-house', 9900, 'index:workbench', '', 'workbench', 'workbench', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (30, 0, 'M', '权限', 'el-icon-lock', 9400, '', '', '', 'auth', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (40, 30, 'C', '管理员', '', 0, 'auth:admin:lists', '', 'auth/admin/index', 'admin', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (41, 40, 'A', '管理员详情', '', 0, 'auth:admin:detail', '', '', '', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (42, 40, 'A', '管理员新增', '', 0, 'auth:admin:add', '', '', '', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (43, 40, 'A', '管理员编辑', '', 0, 'auth:admin:edit', '', '', '', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (44, 40, 'A', '管理员删除', '', 0, 'auth:admin:delete', '', '', '', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (50, 30, 'C', '角色管理', '', 0, 'auth:role:lists', '', 'auth/role/index', 'role', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (51, 50, 'A', '角色详情', '', 0, 'auth:role:detail', '', '', '', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (52, 50, 'A', '角色新增', '', 0, 'auth:role:add', '', '', '', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (53, 50, 'A', '角色编辑', '', 0, 'auth:role:edit', '', '', '', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (55, 50, 'A', '角色删除', '', 0, 'auth:role:delete', '', '', '', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (60, 30, 'C', '菜单管理', '', 0, 'auth:menu:lists', '', 'auth/menu/index', 'menu', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (61, 60, 'A', '菜单详情', '', 0, 'auth:menu:detail', '', '', '', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (62, 60, 'A', '菜单新增', '', 0, 'auth:menu:add', '', '', '', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (63, 60, 'A', '菜单编辑', '', 0, 'auth:menu:edit', '', '', '', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (64, 60, 'A', '菜单删除', '', 0, 'auth:menu:delete', '', '', '', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (70, 30, 'C', '部门管理', '', 0, 'auth:dept:lists', '', 'auth/dept/index', 'dept', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (71, 70, 'A', '部门详情', '', 0, 'auth:dept:detail', '', '', '', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (72, 70, 'A', '部门新增', '', 0, 'auth:dept:add', '', '', '', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (73, 70, 'A', '部门编辑', '', 0, 'auth:dept:edit', '', '', '', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (74, 70, 'A', '部门删除', '', 0, 'auth:dept:delete', '', '', '', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (80, 30, 'C', '岗位管理', '', 0, 'auth:post:lists', '', 'auth/post/index', 'post', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (81, 80, 'A', '岗位详情', '', 0, 'auth:post:detail', '', '', '', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (82, 80, 'A', '岗位新增', '', 0, 'auth:post:add', '', '', '', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (83, 80, 'A', '岗位编辑', '', 0, 'auth:post:edit', '', '', '', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (84, 80, 'A', '岗位删除', '', 0, 'auth:post:delete', '', '', '', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (500, 0, 'M', '设置', 'el-icon-setting', 9300, '', '', '', 'setting', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (510, 500, 'C', '后台设置', '', 0, 'setting:backs:lists', '', 'setting/backs', 'backs', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (512, 510, 'A', '网站配置保存', '', 0, 'setting:backs:save', '', '', '', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (520, 500, 'C', '网站设置', '', 0, 'setting:basics:detail', '', 'setting/basics', 'basics', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (522, 520, 'A', '网站配置保存', '', 0, 'setting:basics:save', '', '', '', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (530, 500, 'C', '登录设置', '', 0, 'setting:login:detail', '', 'setting/login', 'login', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (532, 530, 'A', '登录配置保存', '', 0, 'setting:login:save', '', '', '', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (540, 500, 'C', '渠道设置', '', 0, 'setting:channel:detail', '', 'setting/channel', 'channel', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (542, 540, 'A', '渠道配置保存', '', 0, 'setting:channel:save', '', '', '', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (550, 500, 'C', '协议设置', '', 0, 'setting:policy:detail', '', 'setting/policy', 'policy', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (551, 550, 'A', '政策配置保存', '', 0, 'setting:policy:save', '', '', '', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (560, 500, 'C', '存储设置', '', 0, 'setting:storage:detail', '', 'setting/storage', 'storage', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (562, 560, 'A', '存储配置保存', '', 0, 'setting:storage:save', '', '', '', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (570, 500, 'C', '邮件设置', '', 0, 'setting:email:detail', '', 'setting/email', 'email', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (572, 570, 'A', '邮件配置保存', '', 0, 'setting:email:save', '', '', '', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (580, 500, 'C', '短信设置', '', 0, 'setting:sms:lists', '', 'setting/sms/index', 'sms', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (581, 580, 'A', '短信配置详情', '', 0, 'setting:sms:detail', '', '', '', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (582, 580, 'A', '短信配置保存', '', 0, 'setting:sms:save', '', '', '', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (590, 500, 'C', '通知设置', '', 0, 'setting:notice:detail', '', 'setting/notice/index', 'notice', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (592, 590, 'A', '通知配置保存', '', 0, 'setting:notice:save', '', '', '', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (610, 500, 'C', '支付设置', '', 0, 'setting:payment:lists', '', 'setting/payment/index', 'payment', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (611, 550, 'A', '支付配置详情', '', 0, 'setting:payment:detail', '', '', '', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (612, 550, 'A', '支付配置保存', '', 0, 'setting:payment:save', '', '', '', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (620, 500, 'C', '轮播海报', '', 0, 'setting:banner:lists', '', 'setting/banner/index', 'banner', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (621, 620, 'A', '轮播详情', '', 0, 'setting:banner:detail', '', '', '', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (622, 620, 'A', '轮播新增', '', 0, 'setting:banner:add', '', '', '', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (623, 620, 'A', '轮播编辑', '', 0, 'setting:banner:edit', '', '', '', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (624, 620, 'A', '轮播删除', '', 0, 'setting:banner:delete', '', '', '', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (630, 500, 'C', '友情链接', '', 0, 'setting:links:lists', '', 'setting/links/index', 'links', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (631, 630, 'A', '友链详情', '', 0, 'setting:links:detail', '', '', '', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (632, 630, 'A', '友链新增', '', 0, 'setting:links:add', '', '', '', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (633, 630, 'A', '友链编辑', '', 0, 'setting:links:edit', '', '', '', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (634, 630, 'A', '友链删除', '', 0, 'setting:links:delete', '', '', '', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (3000, 0, 'M', '系统', 'el-icon-ElementPlus', 0, '', '', '', 'system', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (3011, 3000, 'C', '计划任务', '', 0, 'system:crontab:lists', '', 'system/crontab/index', 'crontab', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (3012, 3011, 'A', '任务详情', '', 0, 'system:crontab:detail', '', '', '', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (3013, 3011, 'A', '任务新增', '', 0, 'system:crontab:add', '', '', '', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (3014, 3011, 'A', '任务编辑', '', 0, 'system:crontab:edit', '', '', '', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (3015, 3011, 'A', '任务删除', '', 0, 'system:crontab:delete', '', '', '', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (3016, 3011, 'A', '任务启动', '', 0, 'system:crontab:start', '', '', '', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (3017, 3011, 'A', '任务停止', '', 0, 'system:crontab:stop', '', '', '', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (3030, 3000, 'C', '清除缓存', '', 0, '', '', 'system/clear', 'clear', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (3031, 3030, 'A', '立即清除', '', 0, 'system:clear', '', 'setting/clear', '', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (3040, 3000, 'C', '系统日志', '', 0, 'system:journal:lists', '', 'system/journal/index', 'journal', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (3041, 3040, 'A', '日志详情', '', 0, 'system:journal:detail', '', 'setting/journal', '', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (3500, 3000, 'C', '素材中心', '', 0, '', '', 'system/materials', 'materials', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (3511, 3500, 'A', '附件移动', '', 0, 'attach:album_move', '', '', '', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (3512, 3500, 'A', '附件命名', '', 0, 'attach:album_rename', '', '', '', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (3513, 3500, 'A', '附件删除', '', 0, 'attach:album_delete', '', '', '', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (3521, 3500, 'A', '素材分组创建', '', 0, 'attach:cate_add', '', '', '', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (3522, 3500, 'A', '素材分组命名', '', 0, 'attach:cate_rename', '', '', '', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (3523, 3500, 'A', '素材分组删除', '', 0, 'attach:cate_delete', '', '', '', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (6000, 0, 'M', '内容', 'el-icon-Collection', 9700, '', '', 'setting/journal', 'content', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (6010, 6000, 'C', '分类管理', '', 0, 'content:category:lists', '', 'content/category/index', 'category', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (6011, 6010, 'A', '分类详情', '', 0, 'content:category:detail', '', 'setting/journal', '', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (6012, 6010, 'A', '分类新增', '', 0, 'content:category:add', '', 'setting/journal', '', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (6013, 6010, 'A', '分类编辑', '', 0, 'content:category:edit', '', 'setting/journal', '', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (6014, 6010, 'A', '分类删除', '', 0, 'content:category:delete', '', 'setting/journal', '', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (6020, 6000, 'C', '文章管理', '', 0, 'content:article:lists', '', 'content/article/index', 'article', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (6021, 6020, 'A', '文章详情', '', 0, 'content:article:detail', '', 'setting/journal', '', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (6022, 6020, 'A', '文章新增', '', 0, 'content:article:add', '', 'setting/journal', '', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (6023, 6020, 'A', '文章编辑', '', 0, 'content:article:edit', '', 'setting/journal', '', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (6024, 6020, 'A', '文章删除', '', 0, 'content:article:delete', '', 'setting/journal', '', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (7000, 0, 'M', '用户', 'el-icon-User', 9800, '', '', 'setting/journal', 'user', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (7010, 7000, 'C', '用户管理', '', 0, 'users:user:lists', '', 'user/lists/index', 'lists', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (7011, 7010, 'A', '用户详情', '', 0, 'users:user:detail', '', 'setting/journal', '', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (7012, 7010, 'A', '设置分组', '', 0, 'users:user:set_group', '', 'setting/journal', '', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (7020, 7000, 'C', '用户分组', '', 0, 'users:group:lists', '', 'user/grouping/index', 'grouping', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (7021, 7020, 'A', '分组详情', '', 0, 'users:group:detail', '', 'setting/journal', '', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (7022, 7020, 'A', '分组新增', '', 0, 'users:group:add', '', 'setting/journal', '', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (7023, 7020, 'A', '分组编辑', '', 0, 'users:group:edit', '', 'setting/journal', '', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (7024, 7020, 'A', '分组删除', '', 0, 'users:group:delete', '', 'setting/journal', '', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (7030, 7000, 'C', '用户足迹', '', 0, 'users:visitor:lists', '', 'user/visitor/index', 'visitor', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (7031, 7030, 'A', '足迹详情', '', 0, 'users:visitor:detail', '', 'setting/journal', '', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (8000, 0, 'M', '财务', 'el-icon-SetUp', 9500, '', '', '', 'finance', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (8010, 8000, 'C', '余额明细', '', 0, '', '', 'finance/balance', 'balance', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (8011, 8000, 'C', '充值记录', '', 0, '', '', 'finance/recharge', 'recharge', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (9000, 0, 'M', '营销', 'el-icon-MessageBox', 9600, '', '', '', 'market', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (9010, 9000, 'C', '充值套餐', '', 0, 'market:recharge:lists', '', 'market/recharge/index', 'recharge', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (9011, 9010, 'A', '充值套餐详情', '', 0, 'market:recharge:detail', '', '', '', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (9012, 9010, 'A', '充值套餐新增', '', 0, 'market:recharge:add', '', '', '', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (9013, 9010, 'A', '充值套餐编辑', '', 0, 'market:recharge:edit', '', '', '', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (9014, 9010, 'A', '充值套餐删除', '', 0, 'market:recharge:delete', '', '', '', 1, 0, 0, 1716170400, 1716170400, 0);
INSERT INTO `wait_auth_menu` VALUES (9017, 9010, 'A', '充值参数设置', '', 0, 'market:recharge:config', '', '', '', 1, 0, 0, 1716170400, 1716170400, 0);
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
