# 爬虫接口测试工具使用说明

## 功能说明

这个工具允许你单独测试每个爬虫接口，不依赖消息队列，直接调用 API 获取数据，并可选择保存到MySQL数据库。

## 支持的接口类型

1. **list** - 商品列表（支持保存到数据库）
2. **detail** - 商品详情
3. **trend** - 商品趋势
4. **user-top** - 达人TOP
5. **user-list** - 达人列表
6. **live-trend** - 直播趋势
7. **live-list** - 直播列表
8. **live-relation** - 直播关联
9. **video-sales** - 视频销售
10. **video-list** - 视频列表
11. **video-time** - 视频时间

## 使用方法

### 方法一：使用 .bat 文件（推荐）

```bash
# 查看所有可用接口
test_crawler.bat

# 测试商品列表（第1页）
test_crawler.bat list 1

# 测试商品详情
test_crawler.bat detail 3620889142579355421

# 测试商品趋势
test_crawler.bat trend 3620889142579355421
```

### 方法二：直接使用 Python

```bash
# 查看所有可用接口
python test_crawler.py --list

# 测试商品列表
python test_crawler.py --type list --page 1

# 测试商品列表并保存到数据库
python test_crawler.py --type list --page 1 --save-db

# 测试商品详情
python test_crawler.py --type detail --product-id 3620889142579355421

# 测试商品趋势
python test_crawler.py --type trend --goods-id 3620889142579355421

# 保存结果到文件
python test_crawler.py --type list --page 1 --output result.json

# 同时保存到文件和数据库
python test_crawler.py --type list --page 1 --output result.json --save-db
```

## 参数说明

- `--list` - 显示所有可用的接口
- `--type` - 接口类型（必需）
- `--page` - 页码（仅用于 list 类型，默认为 1）
- `--product-id` - 商品ID（用于 detail 类型）
- `--goods-id` - 商品ID（用于其他类型）
- `--output` - 保存结果到文件（JSON格式）
- `--save-db` - 保存数据到MySQL数据库（仅支持 list 类型）

## 数据库配置

数据库配置在 `test_crawler.py` 文件中：

```python
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '123456',
    'database': 'dy_analysis_system',
    'charset': 'utf8mb4'
}
```

数据表结构定义在 `create_goods_table.sql` 文件中，首次运行时会自动创建表。

## 数据表结构

商品数据保存在 `goods_list` 表中，包含以下主要字段：

- 基本信息：goods_id, product_id, platform, status
- 商品信息：title, cover, url
- 价格信息：price, coupon, coupon_price
- 佣金信息：cos_ratio, cos_fee, kol_cos_fee
- 店铺信息：shop_id, shop_name, shop_logo
- 数据统计：view_num, order_num, sales, sales_24, sales_7day
- JSON字段：labels, tags, imgs, shop_total_score, raw_data

使用 `product_id` 作为唯一键，重复数据会自动更新。

## 输出说明

工具会显示：
- 接口调用结果（成功/失败）
- 获取到的数据数量
- 前5条数据的详细信息
- 如果指定了 `--output`，会将完整结果保存到 JSON 文件
- 如果指定了 `--save-db`，会将数据保存到MySQL数据库

## 注意事项

1. 确保已经配置好抖音 cookies（`douyin_cookies.json`）
2. 确保虚拟环境已经安装（运行过 `setup_env.bat`）
3. 商品ID可以从商品列表接口获取
4. 测试时不会影响消息队列
5. 日志会保存到 `logs/TestCrawler.log`
6. 使用 `--save-db` 前确保MySQL数据库已启动并配置正确
7. 数据库表会在首次使用时自动创建

## 常见问题

### Q: 提示 "未找到虚拟环境"
A: 先运行 `setup_env.bat` 安装虚拟环境

### Q: 提示 "请求失败" 或 "接口返回无数据"
A: 检查 `douyin_cookies.json` 是否有效，可能需要更新 cookies

### Q: 如何获取商品ID？
A: 先运行 `python test_crawler.py --type list --page 1` 获取商品列表，从中复制商品ID

### Q: 数据库连接失败怎么办？
A: 检查 MySQL 是否启动，数据库配置是否正确（host, port, user, password, database）

### Q: 可以同时测试多个接口吗？
A: 可以，每次运行测试一个接口，可以开多个命令行窗口同时测试

### Q: 数据会重复保存吗？
A: 不会，使用 `product_id` 作为唯一键，重复数据会自动更新而不是插入新记录
