# 故障排除指南

## 问题1：前端显示 "toFixed is not a function" 错误

### 症状
- 浏览器控制台显示错误：`(goods.price + goods.coupon).toFixed is not a function`
- 商品列表无法正常显示

### 原因
- MySQL数据库返回的数值字段是字符串类型
- 前端尝试对字符串执行数值操作导致错误

### 解决方案
已在代码中修复：
1. **后端修复**：`backend/routes/goods.py` 现在会自动将所有数值字段转换为正确的类型（float/int）
2. **前端防护**：`frontend/index.html` 添加了 `|| 0` 默认值防护

**无需手动操作**，只需：
1. 重启后端服务（关闭Flask Backend窗口，重新运行 `start.bat`）
2. 刷新浏览器（`Ctrl + F5`）

### 测试API
```bash
# 运行测试脚本验证API返回的数据类型
test_goods_api.bat
```

## 问题2：首页没有显示商品数据

### 原因
- 数据库中没有数据
- 后端服务未重启（新增的goods路由未加载）
- 前端未刷新

### 解决方案

#### 步骤1：确保数据库中有数据
```bash
# 运行爬虫并保存到数据库
python test_crawler.py --type list --page 1 --save-db
```

#### 步骤2：重启后端服务
1. 关闭当前运行的Flask Backend窗口
2. 重新运行 `start.bat` 或单独启动后端：
```bash
.env\Scripts\python.exe backend/app.py
```

#### 步骤3：刷新浏览器
- 按 `Ctrl + F5` 强制刷新页面
- 或清除浏览器缓存后刷新

#### 步骤4：检查浏览器控制台
1. 按 `F12` 打开开发者工具
2. 查看 Console 标签是否有错误
3. 查看 Network 标签，检查 `/api/goods/list` 请求是否成功

### 验证数据库
```bash
# 检查数据库中的商品数量
python -c "import pymysql; conn = pymysql.connect(host='localhost', user='root', password='123456', database='dy_analysis_system'); cursor = conn.cursor(); cursor.execute('SELECT COUNT(*) FROM goods_list'); print('商品总数:', cursor.fetchone()[0])"
```

## 问题3：启动Worker时残留数据导致一直在爬

### 原因
- 上次运行时队列中有未处理完的消息
- Worker会继续处理这些残留消息

### 解决方案

#### 方案1：使用清理模式启动（推荐）
```bash
# 使用 start_clean.bat 启动，会自动清空所有队列
start_clean.bat
```

#### 方案2：手动清理队列
```bash
# 先停止所有Worker
reset_all.bat

# 或者只清理队列
clean_queues.bat
```

#### 方案3：使用reset_all.bat完全重置
```bash
# 停止Worker + 清理队列
reset_all.bat
```

### 预防措施
- 测试完成后及时停止Worker
- 不需要爬取时使用 `reset_all.bat` 清理
- 启动前检查队列状态

## 问题3：API返回401未登录

### 原因
- Token过期或无效
- 未登录

### 解决方案
1. 重新登录系统
2. 检查localStorage中是否有token：
   - 打开浏览器控制台
   - 输入：`localStorage.getItem('token')`
   - 如果为null，需要重新登录

## 问题4：商品图片无法显示

### 原因
- 图片URL失效
- 网络问题

### 解决方案
- 图片加载失败会自动显示占位图
- 检查网络连接
- 重新爬取数据获取新的图片URL

## 常用命令

### 启动相关
```bash
start.bat           # 正常启动（保留队列消息）
start_clean.bat     # 清理模式启动（清空队列）
```

### 停止相关
```bash
reset_all.bat       # 停止Worker + 清理队列
stop_workers.bat    # 只停止Worker
clean_queues.bat    # 只清理队列
```

### 测试相关
```bash
# 测试爬虫并保存
python test_crawler.py --type list --page 1 --save-db

# 只测试不保存
python test_crawler.py --type list --page 1

# 查看所有接口
python test_crawler.py --list
```

## 日志查看

### 后端日志
- 查看Flask Backend窗口的输出

### Worker日志
- 查看Crawler Workers窗口的输出
- 或查看 `logs/` 目录下的日志文件

### 数据库日志
```bash
# 查看最近的商品
python -c "import pymysql; conn = pymysql.connect(host='localhost', user='root', password='123456', database='dy_analysis_system', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor); cursor = conn.cursor(); cursor.execute('SELECT product_id, title, price, created_at FROM goods_list ORDER BY created_at DESC LIMIT 5'); import json; print(json.dumps(cursor.fetchall(), ensure_ascii=False, indent=2, default=str))"
```

## 联系支持

如果以上方法都无法解决问题，请：
1. 检查所有服务是否正常运行
2. 查看日志文件中的错误信息
3. 确认数据库连接正常
4. 确认RabbitMQ服务正常
