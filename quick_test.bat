@echo off
chcp 65001 >nul 2>&1
echo ========================================
echo   快速测试 - 联网搜索 API
echo ========================================
echo.

REM 检查依赖
pip show requests >nul 2>&1
if errorlevel 1 (
    echo 正在安装依赖...
    pip install requests
)

echo 正在运行测试查询...
echo.
python web_search_api.py

echo.
echo 测试完成！
pause
