@echo off
chcp 65001 >nul
echo ========================================
echo 测试商品API
echo ========================================
echo.

.env\Scripts\python.exe test_goods_api.py

echo.
pause
