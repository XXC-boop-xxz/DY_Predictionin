-- 商品列表数据表
CREATE TABLE IF NOT EXISTS `goods_list` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '自增主键',
    
    -- 基本信息
    `goods_id` VARCHAR(64) NOT NULL COMMENT '内部商品ID',
    `product_id` VARCHAR(64) NOT NULL COMMENT '抖音商品ID',
    `platform` VARCHAR(20) DEFAULT 'douyin' COMMENT '平台',
    `status` TINYINT DEFAULT 1 COMMENT '状态',
    
    -- 商品信息
    `title` VARCHAR(500) COMMENT '商品标题',
    `cover` VARCHAR(1000) COMMENT '封面图URL',
    `url` VARCHAR(1000) COMMENT '商品链接',
    
    -- 价格信息
    `price` DECIMAL(10,2) COMMENT '商品价格',
    `coupon` DECIMAL(10,2) DEFAULT 0 COMMENT '优惠券金额',
    `coupon_price` DECIMAL(10,2) COMMENT '券后价格',
    
    -- 佣金信息
    `cos_ratio` DECIMAL(5,4) COMMENT '佣金比例',
    `kol_cos_ratio` DECIMAL(5,4) COMMENT '达人佣金比例',
    `cos_fee` DECIMAL(10,2) COMMENT '佣金金额',
    `kol_cos_fee` DECIMAL(10,2) COMMENT '达人佣金金额',
    
    -- 类目信息
    `cate_0` INT COMMENT '类目0',
    `first_cid` VARCHAR(20) COMMENT '一级类目ID',
    `second_cid` VARCHAR(20) COMMENT '二级类目ID',
    `third_cid` VARCHAR(20) COMMENT '三级类目ID',
    
    -- 补贴信息
    `subsidy_status` TINYINT DEFAULT 0 COMMENT '补贴状态',
    `subsidy_ratio` DECIMAL(5,4) DEFAULT 0 COMMENT '补贴比例',
    `butie_rate` DECIMAL(5,4) DEFAULT 0 COMMENT '补贴率',
    
    -- 其他平台
    `other_platform` TINYINT DEFAULT 0 COMMENT '是否其他平台',
    
    -- 店铺信息
    `shop_id` VARCHAR(64) COMMENT '店铺ID',
    `shop_name` VARCHAR(200) COMMENT '店铺名称',
    `shop_logo` VARCHAR(1000) COMMENT '店铺Logo',
    
    -- 分享和推广
    `sharable` TINYINT DEFAULT 1 COMMENT '是否可分享',
    `is_redu` TINYINT DEFAULT 1 COMMENT '是否热度商品',
    
    -- 时间信息
    `begin_time` DATE COMMENT '开始时间',
    `end_time` DATE COMMENT '结束时间',
    `in_stock` TINYINT DEFAULT 1 COMMENT '是否有货',
    
    -- 数据统计
    `view_num` INT DEFAULT 0 COMMENT '浏览量',
    `order_num` VARCHAR(50) COMMENT '订单数范围',
    `combined` INT DEFAULT 0 COMMENT '综合评分',
    `sales_24` VARCHAR(50) COMMENT '24小时销量',
    `kol_num` VARCHAR(50) COMMENT '达人数量',
    `sales` VARCHAR(50) COMMENT '总销量',
    `is_sole` TINYINT DEFAULT 0 COMMENT '是否独家',
    `sales_7day` VARCHAR(50) COMMENT '7天销量',
    `order_count` INT DEFAULT 0 COMMENT '订单数',
    `pay_amount` DECIMAL(15,2) DEFAULT 0 COMMENT '支付金额',
    `service_fee` DECIMAL(15,2) DEFAULT 0 COMMENT '服务费',
    
    -- 活动信息
    `activity_id` VARCHAR(64) COMMENT '活动ID',
    `kol_weekday` INT DEFAULT 0 COMMENT '达人工作日',
    `said` VARCHAR(64) COMMENT 'SAID',
    `favorite_id` INT DEFAULT 0 COMMENT '收藏ID',
    `issue_ratio` DECIMAL(10,2) DEFAULT 0 COMMENT '问题比例',
    
    -- 标签和标记（JSON存储）
    `labels` JSON COMMENT '标签列表',
    `tags` JSON COMMENT '标记',
    `imgs` JSON COMMENT '图片列表',
    
    -- 店铺评分（JSON存储）
    `shop_total_score` JSON COMMENT '店铺总评分',
    
    -- 原始数据
    `raw_data` JSON COMMENT '原始完整数据',
    
    -- 时间戳
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    
    -- 索引
    INDEX `idx_product_id` (`product_id`),
    INDEX `idx_goods_id` (`goods_id`),
    INDEX `idx_shop_id` (`shop_id`),
    INDEX `idx_activity_id` (`activity_id`),
    INDEX `idx_price` (`price`),
    INDEX `idx_cos_fee` (`cos_fee`),
    INDEX `idx_created_at` (`created_at`),
    UNIQUE KEY `uk_product_id` (`product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='商品列表数据表';
