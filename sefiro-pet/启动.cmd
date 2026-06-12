@echo off
chcp 65001 >nul
title 瑟菲洛桌宠
echo ====================================
echo   瑟菲洛桌宠 v0.1
echo   Esc = 退出 ^| 双击 = 聊天
echo ====================================
echo.

:: 检查Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 没找到Python！请先安装 https://www.python.org/downloads/
    echo    装的时候记得勾 "Add Python to PATH"
    pause
    exit /b
)

:: 检查依赖
python -c "import PIL" >nul 2>&1
if %errorlevel% neq 0 (
    echo 📦 首次运行，安装依赖...
    pip install pillow requests edge-tts pywin32 -q
    echo ✅ 装好了！
    echo.
)

:: 启动
python main.py
pause
