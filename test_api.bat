@echo off
chcp 65001 >nul
echo.
echo ========================================
echo 测试商品API
echo ========================================
echo.

echo 测试1: 不带token（应该返回401）
.env\Scripts\python.exe -c "import requests; r = requests.get('http://localhost:5000/api/goods/list?page=1^&page_size=5'); print('状态码:', r.status_code); print('响应:', r.text[:200])"

echo.
echo.
echo 测试2: 获取token并测试
.env\Scripts\python.exe -c "import requests; session = requests.Session(); login_data = {'username': 'admin', 'password': 'admin123'}; r1 = session.post('http://localhost:5000/api/auth/login', json=login_data); print('登录状态:', r1.status_code); token = r1.json().get('data', {}).get('token'); print('Token:', token[:50] if token else 'None'); r2 = session.get('http://localhost:5000/api/goods/list?page=1^&page_size=5', headers={'Authorization': f'Bearer {token}'}); print('商品API状态:', r2.status_code); print('响应:', r2.text[:500])"

echo.
pause
