# -*- coding: utf-8 -*-
"""
爬虫接口测试工具

功能：
1. 单独测试每个爬虫接口
2. 查看接口返回的数据
3. 不依赖消息队列，直接调用 API

使用方式：
    # 测试商品列表
    python test_crawler.py --type list --page 1
    
    # 测试商品详情
    python test_crawler.py --type detail --product-id 3620889142579355421
    
    # 测试商品趋势
    python test_crawler.py --type trend --goods-id 3620889142579355421
    
    # 查看所有可用接口
    python test_crawler.py --list
"""

import sys
import os
import argparse
import json
import time
import requests
import pymysql

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from logger import init_logger, get_logger
import logging

# 初始化日志
init_logger(log_dir="logs", log_level=logging.INFO)
log = get_logger("TestCrawler")

# 导入 ReduxSigner
from crawler.dy_xingtui.ReduxSiger import ReduxSigner


# API 配置
BASE_URL = "https://www.reduxingtui.com"
BASE_API = "/api/douke/dcc"
TOKEN = "45114cedfddd64db6b0c5f0acf929487"

# 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '123456',
    'database': 'dy_analysis_system',
    'charset': 'utf8mb4'
}


def get_db_connection():
    """获取数据库连接"""
    try:
        conn = pymysql.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        log.error(f"数据库连接失败: {e}")
        return None


def ensure_table_exists():
    """确保数据表存在"""
    try:
        conn = get_db_connection()
        if not conn:
            return False
        
        cursor = conn.cursor()
        
        # 读取SQL文件
        with open('create_goods_table.sql', 'r', encoding='utf-8') as f:
            sql = f.read()
        
        # 执行建表语句
        cursor.execute(sql)
        conn.commit()
        
        cursor.close()
        conn.close()
        
        log.info("数据表检查/创建成功")
        return True
    except Exception as e:
        log.error(f"创建数据表失败: {e}")
        return False


def save_goods_to_db(goods_list):
    """
    保存商品列表到数据库
    
    Args:
        goods_list: 商品列表数据
        
    Returns:
        成功保存的数量
    """
    if not goods_list:
        return 0
    
    try:
        conn = get_db_connection()
        if not conn:
            return 0
        
        cursor = conn.cursor()
        
        # 插入SQL
        insert_sql = """
        INSERT INTO goods_list (
            goods_id, product_id, platform, status,
            title, cover, url,
            price, coupon, coupon_price,
            cos_ratio, kol_cos_ratio, cos_fee, kol_cos_fee,
            cate_0, first_cid, second_cid, third_cid,
            subsidy_status, subsidy_ratio, butie_rate,
            other_platform,
            shop_id, shop_name, shop_logo,
            sharable, is_redu,
            begin_time, end_time, in_stock,
            view_num, order_num, combined, sales_24, kol_num, sales, is_sole, sales_7day,
            order_count, pay_amount, service_fee,
            activity_id, kol_weekday, said, favorite_id, issue_ratio,
            labels, tags, imgs, shop_total_score, raw_data
        ) VALUES (
            %s, %s, %s, %s,
            %s, %s, %s,
            %s, %s, %s,
            %s, %s, %s, %s,
            %s, %s, %s, %s,
            %s, %s, %s,
            %s,
            %s, %s, %s,
            %s, %s,
            %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s
        ) ON DUPLICATE KEY UPDATE
            title = VALUES(title),
            cover = VALUES(cover),
            url = VALUES(url),
            price = VALUES(price),
            coupon = VALUES(coupon),
            coupon_price = VALUES(coupon_price),
            cos_ratio = VALUES(cos_ratio),
            kol_cos_ratio = VALUES(kol_cos_ratio),
            cos_fee = VALUES(cos_fee),
            kol_cos_fee = VALUES(kol_cos_fee),
            shop_name = VALUES(shop_name),
            shop_logo = VALUES(shop_logo),
            view_num = VALUES(view_num),
            order_num = VALUES(order_num),
            combined = VALUES(combined),
            sales_24 = VALUES(sales_24),
            kol_num = VALUES(kol_num),
            sales = VALUES(sales),
            sales_7day = VALUES(sales_7day),
            labels = VALUES(labels),
            tags = VALUES(tags),
            raw_data = VALUES(raw_data),
            updated_at = CURRENT_TIMESTAMP
        """
        
        success_count = 0
        
        for goods in goods_list:
            try:
                # 准备数据
                data = (
                    goods.get('id'),
                    goods.get('product_id'),
                    goods.get('platform', 'douyin'),
                    goods.get('status', 1),
                    
                    goods.get('title'),
                    goods.get('cover'),
                    goods.get('url'),
                    
                    goods.get('price'),
                    goods.get('coupon', 0),
                    goods.get('coupon_price'),
                    
                    goods.get('cos_ratio'),
                    goods.get('kol_cos_ratio'),
                    goods.get('cos_fee'),
                    goods.get('kol_cos_fee'),
                    
                    goods.get('cate_0'),
                    goods.get('first_cid'),
                    goods.get('second_cid'),
                    goods.get('third_cid'),
                    
                    goods.get('subsidy_status', 0),
                    goods.get('subsidy_ratio', 0),
                    goods.get('butie_rate', 0),
                    
                    1 if goods.get('other_platform') else 0,
                    
                    goods.get('shop_id'),
                    goods.get('shop_name'),
                    goods.get('shop_logo'),
                    
                    goods.get('sharable', 1),
                    goods.get('is_redu', 1),
                    
                    goods.get('begin_time'),
                    goods.get('end_time'),
                    1 if goods.get('in_stock') else 0,
                    
                    goods.get('view_num', 0),
                    goods.get('order_num'),
                    goods.get('combined', 0),
                    goods.get('sales_24'),
                    goods.get('kol_num'),
                    goods.get('sales'),
                    goods.get('is_sole', 0),
                    goods.get('sales_7day'),
                    
                    goods.get('order_count', 0),
                    goods.get('pay_amount', 0),
                    goods.get('service_fee', 0),
                    
                    goods.get('activity_id'),
                    goods.get('kol_weekday', 0),
                    goods.get('said'),
                    goods.get('favorite_id', 0),
                    goods.get('issue_ratio', 0),
                    
                    json.dumps(goods.get('labels', []), ensure_ascii=False),
                    json.dumps(goods.get('tags', {}), ensure_ascii=False),
                    json.dumps(goods.get('imgs', []), ensure_ascii=False),
                    json.dumps(goods.get('shop_total_score', {}), ensure_ascii=False),
                    json.dumps(goods, ensure_ascii=False)
                )
                
                cursor.execute(insert_sql, data)
                success_count += 1
                
            except Exception as e:
                log.error(f"保存商品失败 {goods.get('product_id')}: {e}")
                continue
        
        conn.commit()
        cursor.close()
        conn.close()
        
        log.info(f"成功保存 {success_count}/{len(goods_list)} 个商品到数据库")
        return success_count
        
    except Exception as e:
        log.error(f"保存数据到数据库失败: {e}", exc_info=True)
        return 0

def load_cookies():
    """加载 cookies"""
    try:
        with open('douyin_cookies.json', 'r', encoding='utf-8') as f:
            cookies_list = json.load(f)
        
        # 转换为 requests 可用的格式
        cookies = {}
        for cookie in cookies_list:
            cookies[cookie['name']] = cookie['value']
        
        log.info(f"成功加载 {len(cookies)} 个 cookies")
        return cookies
    except Exception as e:
        log.warning(f"加载 cookies 失败: {e}")
        return {}


def call_api(api_path, params):
    """
    调用 API 接口
    
    Args:
        api_path: API 路径（如 /goodsTrend）
        params: 请求参数
        
    Returns:
        响应数据
    """
    try:
        # 加载 cookies
        cookies = load_cookies()
        
        # 添加 token
        params['token'] = TOKEN
        
        # 生成签名
        sign_data = ReduxSigner.get_siger_by_params(params)
        params['sign'] = sign_data['url_sign']
        params['time'] = sign_data['timestamp']
        
        # 构建请求头
        headers = ReduxSigner.get_headers(sign_data['header_sign'], sign_data['timestamp'], TOKEN)
        
        # 发送请求
        full_path = f"{BASE_API}{api_path}"
        url = f"{BASE_URL}{full_path}"
        log.info(f"请求 URL: {url}")
        log.info(f"请求参数: {params}")
        
        response = requests.get(url, params=params, headers=headers, cookies=cookies, timeout=10)
        
        print(f"响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                print(f"响应内容: {json.dumps(result, ensure_ascii=False, indent=2)[:1000]}...")
            except:
                print(f"响应文本: {response.text[:500]}")
                print(f"\n✗ 响应不是有效的 JSON")
                return None
            
            if result.get('status_code') == 0:
                return result.get('data')
            else:
                log.error(f"API 返回错误")
                print(f"\n✗ API 返回错误")
                print(f"status_code: {result.get('status_code')}")
                print(f"status_msg: {result.get('status_msg', '未知错误')}")
                return None
        else:
            log.error(f"HTTP 请求失败: {response.status_code}")
            print(f"\n✗ HTTP 请求失败: {response.status_code}")
            print(f"响应内容: {response.text[:500]}")
            return None
            
    except Exception as e:
        log.error(f"API 调用失败: {e}", exc_info=True)
        return None


# 所有可用的接口
AVAILABLE_HANDLERS = {
    'list': {
        'name': '商品列表',
        'api_path': None,  # 使用特殊处理
        'params': ['page'],
        'example': 'python test_crawler.py --type list --page 1'
    },
    'detail': {
        'name': '商品详情',
        'api_path': None,  # 使用特殊处理
        'params': ['product_id'],
        'example': 'python test_crawler.py --type detail --product-id 3620889142579355421'
    },
    'trend': {
        'name': '商品趋势',
        'api_path': '/goodsTrend',
        'params': ['goods_id'],
        'example': 'python test_crawler.py --type trend --goods-id 3620889142579355421'
    },
    'user-top': {
        'name': '达人TOP',
        'api_path': '/goodsUserTop',
        'params': ['goods_id'],
        'example': 'python test_crawler.py --type user-top --goods-id 3620889142579355421'
    },
    'user-list': {
        'name': '达人列表',
        'api_path': '/goodsUserList',
        'params': ['goods_id'],
        'example': 'python test_crawler.py --type user-list --goods-id 3620889142579355421'
    },
    'live-trend': {
        'name': '直播趋势',
        'api_path': '/goodsLiveSalesTrend',
        'params': ['goods_id'],
        'example': 'python test_crawler.py --type live-trend --goods-id 3620889142579355421'
    },
    'live-list': {
        'name': '直播列表',
        'api_path': '/goodsLiveList',
        'params': ['goods_id'],
        'example': 'python test_crawler.py --type live-list --goods-id 3620889142579355421'
    },
    'live-relation': {
        'name': '直播关联',
        'api_path': '/goodsLiveRelation',
        'params': ['goods_id'],
        'example': 'python test_crawler.py --type live-relation --goods-id 3620889142579355421'
    },
    'video-sales': {
        'name': '视频销售',
        'api_path': '/goodsVideosales',
        'params': ['goods_id'],
        'example': 'python test_crawler.py --type video-sales --goods-id 3620889142579355421'
    },
    'video-list': {
        'name': '视频列表',
        'api_path': '/goodsVideoList',
        'params': ['goods_id'],
        'example': 'python test_crawler.py --type video-list --goods-id 3620889142579355421'
    },
    'video-time': {
        'name': '视频时间',
        'api_path': '/goodsVideoTime',
        'params': ['goods_id'],
        'example': 'python test_crawler.py --type video-time --goods-id 3620889142579355421'
    }
}


def show_available_handlers():
    """显示所有可用的接口"""
    print("\n" + "=" * 60)
    print("可用的爬虫接口")
    print("=" * 60)
    for key, info in AVAILABLE_HANDLERS.items():
        print(f"\n类型: {key}")
        print(f"名称: {info['name']}")
        print(f"参数: {', '.join(info['params'])}")
        print(f"示例: {info['example']}")
    print("\n" + "=" * 60)


def test_list(page=1, save_db=False):
    """测试商品列表接口"""
    print(f"\n{'=' * 60}")
    print(f"测试商品列表 - 第 {page} 页")
    print("=" * 60)
    
    try:
        # 加载 cookies
        cookies = load_cookies()
        
        # 使用 ReduxSigner 调用商品列表接口
        token = "45114cedfddd64db6b0c5f0acf929487"
        api_path = "/api/douke/goodsParticiple"
        
        # 构建请求参数
        params = {
            "page": page,
            "limit": 20,
            "type": 2,
            "platform": "douyin",
            "title": "",
            "search_type": 11,
            "sort_type": 1,
            "cos_ratio_min": "",
            "cos_ratio_max": "",
            "cos_fee_min": "",
            "cos_fee_max": "",
            "price_min": "",
            "price_max": "",
            "sell_num_min": "",
            "sell_num_max": "",
            "source": 1
        }
        
        print("正在生成签名...")
        # 生成签名
        sign_data = ReduxSigner.get_siger_by_params(params)
        params['sign'] = sign_data['url_sign']
        params['time'] = sign_data['timestamp']
        
        # 构建请求头
        headers = ReduxSigner.get_headers(sign_data['header_sign'], sign_data['timestamp'], token)
        
        # 发送请求
        url = f"https://www.reduxingtui.com{api_path}"
        print(f"正在请求: {url}")
        print(f"请求参数: {params}")
        response = requests.get(url, params=params, headers=headers, cookies=cookies, timeout=10)
        
        print(f"响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                # print(f"响应内容: {json.dumps(result, ensure_ascii=False, indent=2)[:1000]}...")
            except:
                print(f"响应文本: {response.text[:500]}")
                print("响应不是有效的 JSON")
                return None
            
            # 检查响应格式（reduxingtui API 直接返回 data，没有 status_code）
            if 'data' in result or 'list' in result:
                # 提取商品列表
                if 'data' in result:
                    products = result['data'] if isinstance(result['data'], list) else result['data'].get('list', result['data'].get('data', []))
                else:
                    products = result.get('list', [])
                
                print(f"\n成功获取 {len(products)} 个商品\n")
                
                for i, product in enumerate(products[:5], 1):  # 只显示前5个
                    print(f"{i}. 商品ID: {product.get('product_id', product.get('id', 'N/A'))}")
                    print(f"   商品名称: {product.get('product_name', product.get('title', 'N/A'))[:50]}")
                    print(f"   价格: {product.get('price', product.get('cos_fee', 0))} 元")
                    print(f"   销量: {product.get('sales', product.get('sell_num', 0))}")
                    print(f"   佣金: {product.get('cos_fee', 0)} 元")
                    print()
                
                if len(products) > 5:
                    print(f"... 还有 {len(products) - 5} 个商品\n")
                
                # 保存到数据库
                if save_db:
                    print("正在保存到数据库...")
                    # 确保表存在
                    if ensure_table_exists():
                        saved_count = save_goods_to_db(products)
                        print(f"成功保存 {saved_count} 个商品到数据库")
                    else:
                        print("数据表创建失败，无法保存")
                
                return result
            else:
                print("接口返回错误")
                print(f"响应内容: {json.dumps(result, ensure_ascii=False, indent=2)[:500]}")
                return None
        else:
            print(f"\n✗ HTTP 请求失败: {response.status_code}")
            print(f"响应内容: {response.text[:500]}")
            return None
            
    except Exception as e:
        log.error(f"测试失败: {e}", exc_info=True)
        print(f"\n✗ 测试失败: {e}")
        return None


def test_detail(product_id):
    """测试商品详情接口"""
    print(f"\n{'=' * 60}")
    print(f"测试商品详情 - {product_id}")
    print("=" * 60)
    
    try:
        # 加载 cookies
        cookies = load_cookies()
        
        # 使用 ReduxSigner 调用商品详情接口
        token = "45114cedfddd64db6b0c5f0acf929487"
        api_path = "/api/douke/goodsDetail"
        
        # 构建请求参数
        params = {
            "id": product_id,
            "platform": "douyin"
        }
        
        print("正在生成签名...")
        # 生成签名
        sign_data = ReduxSigner.get_siger_by_params(params)
        params['sign'] = sign_data['url_sign']
        params['time'] = sign_data['timestamp']
        
        # 构建请求头
        headers = ReduxSigner.get_headers(sign_data['header_sign'], sign_data['timestamp'], token)
        
        # 发送请求
        url = f"https://www.reduxingtui.com{api_path}"
        print(f"正在请求: {url}")
        print(f"请求参数: {params}")
        response = requests.get(url, params=params, headers=headers, cookies=cookies, timeout=10)
        
        print(f"响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                print(f"响应内容: {json.dumps(result, ensure_ascii=False, indent=2)[:1000]}...")
            except:
                print(f"响应文本: {response.text[:500]}")
                print(f"\n✗ 响应不是有效的 JSON")
                return None
            
            if result.get('status_code') == 0 and 'data' in result:
                data = result['data']
                print(f"\n✓ 成功获取商品详情\n")
                print(f"商品ID: {data.get('product_id', data.get('id', 'N/A'))}")
                print(f"商品名称: {data.get('product_name', data.get('title', 'N/A'))}")
                print(f"价格: ¥{data.get('price', data.get('cos_fee', 0))}")
                print(f"销量: {data.get('sales', data.get('sell_num', 0))}")
                print(f"店铺名称: {data.get('shop_name', 'N/A')}")
                print()
                
                return data
            else:
                print(f"\n✗ 接口返回错误")
                print(f"status_code: {result.get('status_code')}")
                print(f"status_msg: {result.get('status_msg', result.get('msg', '未知错误'))}")
                print(f"完整响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
                return None
                print(f"\n✗ 响应不是有效的 JSON")
                return None
            if result.get('status_code') == 0 and 'data' in result:
                data = result['data']
                print(f"\n✓ 成功获取商品详情\n")
                print(f"商品ID: {data.get('product_id', 'N/A')}")
                print(f"商品名称: {data.get('product_name', 'N/A')}")
                print(f"价格: ¥{data.get('price', 0) / 100:.2f}")
                print(f"销量: {data.get('sales', 0)}")
                print(f"店铺名称: {data.get('shop_name', 'N/A')}")
                print(f"类目: {data.get('first_cname', 'N/A')} > {data.get('second_cname', 'N/A')}")
                print()
                
                return data
            else:
                print(f"\n✗ 接口返回错误")
                print(f"status_code: {result.get('status_code')}")
                print(f"status_msg: {result.get('status_msg', '未知错误')}")
                print(f"完整响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
                return None
        else:
            print(f"\n✗ HTTP 请求失败: {response.status_code}")
            print(f"响应内容: {response.text[:500]}")
            return None
            
    except Exception as e:
        log.error(f"测试失败: {e}", exc_info=True)
        print(f"\n✗ 测试失败: {e}")
        return None


def test_analysis_api(api_path, goods_id, api_name):
    """测试分析类 API"""
    print(f"\n{'=' * 60}")
    print(f"测试{api_name} - {goods_id}")
    print("=" * 60)
    
    try:
        # 构建请求参数
        params = {
            'goods_id': goods_id,
            'start_time': int((time.time() - 30 * 24 * 3600) * 1000),  # 30天前
            'end_time': int(time.time() * 1000)  # 现在
        }
        
        # 调用 API
        result = call_api(api_path, params)
        
        if result:
            # 判断结果类型
            if isinstance(result, dict):
                # 尝试提取列表数据
                data = result.get('result', result.get('list', result.get('trend', result)))
            else:
                data = result
            
            if isinstance(data, list):
                print(f"\n✓ 成功获取 {len(data)} 条数据\n")
                
                # 显示前3条
                for i, item in enumerate(data[:3], 1):
                    print(f"{i}. {json.dumps(item, ensure_ascii=False, indent=2)}")
                    print()
                
                if len(data) > 3:
                    print(f"... 还有 {len(data) - 3} 条数据\n")
            else:
                print(f"\n✓ 成功获取数据\n")
                print(json.dumps(data, ensure_ascii=False, indent=2))
                print()
            
            return result
        else:
            print(f"\n✗ 未获取到数据")
            return None
            
    except Exception as e:
        log.error(f"测试失败: {e}", exc_info=True)
        print(f"\n✗ 测试失败: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(
        description='爬虫接口测试工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 查看所有可用接口
  python test_crawler.py --list
  
  # 测试商品列表
  python test_crawler.py --type list --page 1
  
  # 测试商品详情
  python test_crawler.py --type detail --product-id 3620889142579355421
  
  # 测试商品趋势
  python test_crawler.py --type trend --goods-id 3620889142579355421
  
  # 保存结果到文件
  python test_crawler.py --type list --page 1 --output result.json
        """
    )
    
    parser.add_argument('--list', action='store_true', help='显示所有可用的接口')
    parser.add_argument('--type', type=str, help='接口类型')
    parser.add_argument('--page', type=int, default=1, help='页码（用于 list 类型）')
    parser.add_argument('--product-id', type=str, help='商品ID（用于 detail 类型）')
    parser.add_argument('--goods-id', type=str, help='商品ID（用于其他类型）')
    parser.add_argument('--output', type=str, help='保存结果到文件（JSON格式）')
    parser.add_argument('--save-db', action='store_true', help='保存数据到MySQL数据库')
    
    args = parser.parse_args()
    
    # 显示所有可用接口
    if args.list:
        show_available_handlers()
        return
    
    # 检查是否指定了类型
    if not args.type:
        parser.print_help()
        return
    
    # 检查类型是否有效
    if args.type not in AVAILABLE_HANDLERS:
        print(f"\n✗ 无效的接口类型: {args.type}")
        print(f"使用 --list 查看所有可用接口")
        return
    
    # 执行测试
    result = None
    
    if args.type == 'list':
        result = test_list(page=args.page, save_db=args.save_db)
    
    elif args.type == 'detail':
        if not args.product_id:
            print("\n✗ 缺少参数: --product-id")
            return
        result = test_detail(product_id=args.product_id)
    
    else:
        # 使用分析 API 测试
        if not args.goods_id:
            print("\n✗ 缺少参数: --goods-id")
            return
        
        handler_info = AVAILABLE_HANDLERS[args.type]
        api_path = handler_info['api_path']
        api_name = handler_info['name']
        
        result = test_analysis_api(api_path, args.goods_id, api_name)
    
    # 保存结果到文件
    if result and args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            print(f"\n✓ 结果已保存到: {args.output}")
        except Exception as e:
            print(f"\n✗ 保存失败: {e}")
    
    print("\n" + "=" * 60)


if __name__ == '__main__':
    main()
