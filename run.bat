@echo off
chcp 65001 >nul 2>&1
REM 联网搜索 API 快速启动脚本
echo ========================================
echo   联网搜索 API 配置和运行助手
echo ========================================
echo.

REM 检查 Python 是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python，请先安装 Python 3.7+
    pause
    exit /b 1
)

echo [1/4] 检查 Python 环境... OK
echo.

REM 检查依赖
echo [2/4] 检查依赖包...
pip show requests >nul 2>&1
if errorlevel 1 (
    echo 正在安装依赖包...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [错误] 依赖安装失败
        pause
        exit /b 1
    )
) else (
    echo 依赖包已安装
)
echo.

REM 检查配置文件
echo [3/4] 检查配置文件...
if not exist .env (
    echo [警告] 未找到 .env 配置文件
    echo 正在从 .env.example 创建...
    if exist .env.example (
        copy .env.example .env >nul
        echo [完成] 已创建 .env 文件
        echo.
        echo ========================================
        echo   重要: 请编辑 .env 文件并填入您的 API Key
        echo ========================================
        echo.
        echo 按任意键打开 .env 文件进行编辑...
        pause >nul
        notepad .env
    ) else (
        echo [错误] 未找到 .env.example 文件
        pause
        exit /b 1
    )
) else (
    echo 配置文件已存在
)
echo.

REM 运行脚本
echo [4/4] 启动脚本...
echo.
echo ========================================
echo 选择运行模式:
echo   1. 运行示例查询
echo   2. 交互模式
echo   3. 退出
echo ========================================
echo.

set /p choice="请选择 (1/2/3): "

if "%choice%"=="1" (
    echo.
    echo 运行示例查询...
    python web_search_api_env.py
) else if "%choice%"=="2" (
    echo.
    echo 进入交互模式...
    python web_search_api_env.py --interactive
) else (
    echo 退出
    exit /b 0
)

echo.
echo ========================================
echo   执行完成
echo ========================================
pause
