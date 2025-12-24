@echo off
chcp 65001 >nul

echo 正在创建Python虚拟环境...
python -m venv .env

echo 激活虚拟环境...
call .env\Scripts\activate.bat

echo 升级pip...
python -m pip install --upgrade pip

echo 安装依赖包...
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

echo 环境配置完成！
echo 使用 '.env\Scripts\activate.bat' 激活环境
echo 使用 'deactivate' 退出环境
pause