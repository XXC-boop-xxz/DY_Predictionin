#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试商品API
"""

import requests
import json

# 配置
BASE_URL = "http://127.0.0.1:5000"

def test_goods_list():
    """测试商品列表API"""
    print("=" * 60)
    print("测试商品列表API")
    print("=" * 60)
    
    url = f"{BASE_URL}/api/goods/list"
    params = {
        'page': 1,
        'page_size': 5,
        'sort_by': 'created_at',
        'order': 'desc'
    }
    
    try:
        response = requests.get(url, params=params)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"响应: {json.dumps(data, indent=2, ensure_ascii=False)}")
            
            if data.get('code') == 0:
                goods_list = data['data']['list']
                print(f"\n✓ 成功获取 {len(goods_list)} 条商品数据")
                
                if goods_list:
                    print("\n第一条商品数据:")
                    first_goods = goods_list[0]
                    print(f"  商品ID: {first_goods.get('product_id')}")
                    print(f"  标题: {first_goods.get('title')}")
                    print(f"  价格: {first_goods.get('price')} (类型: {type(first_goods.get('price')).__name__})")
                    print(f"  优惠券: {first_goods.get('coupon')} (类型: {type(first_goods.get('coupon')).__name__})")
                    print(f"  佣金: {first_goods.get('cos_fee')} (类型: {type(first_goods.get('cos_fee')).__name__})")
                    print(f"  销量: {first_goods.get('sales')} (类型: {type(first_goods.get('sales')).__name__})")
            else:
                print(f"✗ API返回错误: {data.get('msg')}")
        else:
            print(f"✗ HTTP错误: {response.text}")
            
    except Exception as e:
        print(f"✗ 请求失败: {e}")

def test_goods_stats():
    """测试商品统计API"""
    print("\n" + "=" * 60)
    print("测试商品统计API")
    print("=" * 60)
    
    url = f"{BASE_URL}/api/goods/stats"
    
    try:
        response = requests.get(url)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"响应: {json.dumps(data, indent=2, ensure_ascii=False)}")
            
            if data.get('code') == 0:
                stats = data['data']
                print(f"\n✓ 统计数据:")
                print(f"  商品总数: {stats.get('total_goods')}")
                print(f"  今日新增: {stats.get('today_count')}")
                print(f"  平均价格: {stats.get('avg_price')}")
                print(f"  平均佣金: {stats.get('avg_commission')}")
            else:
                print(f"✗ API返回错误: {data.get('msg')}")
        else:
            print(f"✗ HTTP错误: {response.text}")
            
    except Exception as e:
        print(f"✗ 请求失败: {e}")

if __name__ == '__main__':
    print("注意: 此测试需要后端服务运行在 http://127.0.0.1:5000")
    print("注意: 此测试不需要登录token (仅用于调试)\n")
    
    test_goods_list()
    test_goods_stats()
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)
