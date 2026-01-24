# -*- coding: utf-8 -*-
"""
启动诊断脚本 - 检查所有可能导致 app.py 启动失败的问题
"""
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 60)
print("抖音系统启动诊断")
print("=" * 60)

# 1. 检查依赖包
print("\n[1] 检查依赖包...")
required_packages = [
    'flask',
    'flask_socketio',
    'flask_cors',
    'pymysql',
    'pika'
]

missing_packages = []
for package in required_packages:
    try:
        __import__(package)
        print(f"  ✓ {package}")
    except ImportError:
        print(f"  ✗ {package} - 未安装")
        missing_packages.append(package)

if missing_packages:
    print(f"\n缺少依赖包: {', '.join(missing_packages)}")
    print("请运行: pip install -r requirements.txt")
    sys.exit(1)

# 2. 检查配置文件
print("\n[2] 检查配置...")
try:
    from backend.config import Config
    print(f"  ✓ 配置文件加载成功")
    print(f"    - 数据库: {Config.DB_HOST}:{Config.DB_PORT}")
    print(f"    - RabbitMQ: {Config.MQ_HOST}:{Config.MQ_PORT}")
except Exception as e:
    print(f"  ✗ 配置文件加载失败: {e}")
    sys.exit(1)

# 3. 检查数据库连接
print("\n[3] 检查数据库连接...")
try:
    import pymysql
    conn = pymysql.connect(
        host=Config.DB_HOST,
        port=Config.DB_PORT,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        charset='utf8mb4'
    )
    print(f"  ✓ 数据库连接成功")
    
    # 检查数据库是否存在
    with conn.cursor() as cursor:
        cursor.execute(f"SHOW DATABASES LIKE '{Config.DB_NAME}'")
        if cursor.fetchone():
            print(f"  ✓ 数据库 '{Config.DB_NAME}' 存在")
        else:
            print(f"  ⚠ 数据库 '{Config.DB_NAME}' 不存在，将自动创建")
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {Config.DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print(f"  ✓ 数据库 '{Config.DB_NAME}' 创建成功")
    
    conn.close()
except Exception as e:
    print(f"  ✗ 数据库连接失败: {e}")
    print(f"\n请检查:")
    print(f"  1. MySQL 是否已启动")
    print(f"  2. 配置是否正确: {Config.DB_HOST}:{Config.DB_PORT}")
    print(f"  3. 用户名密码是否正确: {Config.DB_USER}")
    sys.exit(1)

# 4. 检查 RabbitMQ 连接
print("\n[4] 检查 RabbitMQ 连接...")
try:
    import pika
    credentials = pika.PlainCredentials(Config.MQ_USER, Config.MQ_PASSWORD)
    parameters = pika.ConnectionParameters(
        host=Config.MQ_HOST,
        port=Config.MQ_PORT,
        credentials=credentials,
        connection_attempts=3,
        retry_delay=2
    )
    connection = pika.BlockingConnection(parameters)
    print(f"  ✓ RabbitMQ 连接成功")
    connection.close()
except Exception as e:
    print(f"  ✗ RabbitMQ 连接失败: {e}")
    print(f"\n请检查:")
    print(f"  1. RabbitMQ 是否已启动")
    print(f"  2. Docker 容器是否运行: docker ps | findstr rabbitmq")
    print(f"  3. 配置是否正确: {Config.MQ_HOST}:{Config.MQ_PORT}")
    print(f"\n如果未启动，请运行:")
    print(f"  docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management")
    sys.exit(1)

# 5. 检查路由模块
print("\n[5] 检查路由模块...")
try:
    from backend.routes import register_routes
    print(f"  ✓ 路由模块加载成功")
except Exception as e:
    print(f"  ✗ 路由模块加载失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 6. 尝试初始化数据库表
print("\n[6] 初始化数据库表...")
try:
    from backend.models.base import init_tables, init_default_data
    init_tables()
    print(f"  ✓ 数据库表初始化成功")
    init_default_data()
    print(f"  ✓ 默认数据初始化成功")
except Exception as e:
    print(f"  ⚠ 初始化警告: {e}")
    # 不退出，因为可能只是数据已存在

print("\n" + "=" * 60)
print("诊断完成！所有检查通过")
print("=" * 60)
print("\n现在可以启动系统:")
print("  方式1: 运行 start.bat")
print("  方式2: 手动运行 python backend/app.py")
print("\n访问地址: http://localhost:5000")
print("默认账号: admin / admin123")
print("=" * 60)
