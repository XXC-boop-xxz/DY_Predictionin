@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo.
echo ============================================================
echo 爬虫接口测试工具
echo ============================================================
echo.

REM 检查虚拟环境
if not exist ".env\Scripts\python.exe" (
    echo [错误] 未找到虚拟环境，请先运行 setup_env.bat
    pause
    exit /b 1
)

REM 如果没有参数，显示帮助
if "%~1"=="" (
    .env\Scripts\python.exe test_crawler.py --list
    echo.
    echo 使用示例:
    echo   test_crawler.bat list 1                      # 测试商品列表第1页
    echo   test_crawler.bat detail 3620889142579355421  # 测试商品详情
    echo   test_crawler.bat trend 3620889142579355421   # 测试商品趋势
    echo   test_crawler.bat user-top 3620889142579355421   # 测试达人TOP
    echo   test_crawler.bat user-list 3620889142579355421  # 测试达人列表
    echo   test_crawler.bat live-trend 3620889142579355421 # 测试直播趋势
    echo   test_crawler.bat video-list 3620889142579355421 # 测试视频列表
    echo.
    pause
    exit /b 0
)

REM 根据参数调用测试脚本
if "%~1"=="list" (
    set PAGE=%~2
    if "!PAGE!"=="" set PAGE=1
    .env\Scripts\python.exe test_crawler.py --type list --page !PAGE!
) else if "%~1"=="detail" (
    if "%~2"=="" (
        echo [错误] 缺少商品ID参数
        pause
        exit /b 1
    )
    .env\Scripts\python.exe test_crawler.py --type detail --product-id %~2
) else if "%~1"=="trend" (
    if "%~2"=="" (
        echo [错误] 缺少商品ID参数
        pause
        exit /b 1
    )
    .env\Scripts\python.exe test_crawler.py --type trend --goods-id %~2
) else if "%~1"=="user-top" (
    if "%~2"=="" (
        echo [错误] 缺少商品ID参数
        pause
        exit /b 1
    )
    .env\Scripts\python.exe test_crawler.py --type user-top --goods-id %~2
) else if "%~1"=="user-list" (
    if "%~2"=="" (
        echo [错误] 缺少商品ID参数
        pause
        exit /b 1
    )
    .env\Scripts\python.exe test_crawler.py --type user-list --goods-id %~2
) else if "%~1"=="live-trend" (
    if "%~2"=="" (
        echo [错误] 缺少商品ID参数
        pause
        exit /b 1
    )
    .env\Scripts\python.exe test_crawler.py --type live-trend --goods-id %~2
) else if "%~1"=="live-list" (
    if "%~2"=="" (
        echo [错误] 缺少商品ID参数
        pause
        exit /b 1
    )
    .env\Scripts\python.exe test_crawler.py --type live-list --goods-id %~2
) else if "%~1"=="live-relation" (
    if "%~2"=="" (
        echo [错误] 缺少商品ID参数
        pause
        exit /b 1
    )
    .env\Scripts\python.exe test_crawler.py --type live-relation --goods-id %~2
) else if "%~1"=="video-sales" (
    if "%~2"=="" (
        echo [错误] 缺少商品ID参数
        pause
        exit /b 1
    )
    .env\Scripts\python.exe test_crawler.py --type video-sales --goods-id %~2
) else if "%~1"=="video-list" (
    if "%~2"=="" (
        echo [错误] 缺少商品ID参数
        pause
        exit /b 1
    )
    .env\Scripts\python.exe test_crawler.py --type video-list --goods-id %~2
) else if "%~1"=="video-time" (
    if "%~2"=="" (
        echo [错误] 缺少商品ID参数
        pause
        exit /b 1
    )
    .env\Scripts\python.exe test_crawler.py --type video-time --goods-id %~2
) else if "%~1"=="comment" (
    if "%~2"=="" (
        echo [错误] 缺少商品ID参数
        pause
        exit /b 1
    )
    .env\Scripts\python.exe test_crawler.py --type comment --goods-id %~2
) else (
    echo [错误] 未知的测试类型: %~1
    echo.
    .env\Scripts\python.exe test_crawler.py --list
)

echo.
pause
