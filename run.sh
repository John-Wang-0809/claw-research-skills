#!/bin/bash
# 联网搜索 API 快速启动脚本 (Linux/macOS)

echo "========================================"
echo "  联网搜索 API 配置和运行助手"
echo "========================================"
echo ""

# 检查 Python 是否安装
if ! command -v python3 &> /dev/null; then
    echo "[错误] 未找到 Python3，请先安装 Python 3.7+"
    exit 1
fi

echo "[1/4] 检查 Python 环境... OK"
echo ""

# 检查依赖
echo "[2/4] 检查依赖包..."
if ! python3 -c "import requests" &> /dev/null; then
    echo "正在安装依赖包..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "[错误] 依赖安装失败"
        exit 1
    fi
else
    echo "依赖包已安装"
fi
echo ""

# 检查配置文件
echo "[3/4] 检查配置文件..."
if [ ! -f .env ]; then
    echo "[警告] 未找到 .env 配置文件"
    if [ -f .env.example ]; then
        echo "正在从 .env.example 创建..."
        cp .env.example .env
        echo "[完成] 已创建 .env 文件"
        echo ""
        echo "========================================"
        echo "  重要: 请编辑 .env 文件并填入您的 API Key"
        echo "========================================"
        echo ""
        echo "按 Enter 键打开 .env 文件进行编辑..."
        read
        ${EDITOR:-nano} .env
    else
        echo "[错误] 未找到 .env.example 文件"
        exit 1
    fi
else
    echo "配置文件已存在"
fi
echo ""

# 运行脚本
echo "[4/4] 启动脚本..."
echo ""
echo "========================================"
echo "选择运行模式:"
echo "  1. 运行示例查询"
echo "  2. 交互模式"
echo "  3. 退出"
echo "========================================"
echo ""

read -p "请选择 (1/2/3): " choice

case $choice in
    1)
        echo ""
        echo "运行示例查询..."
        python3 web_search_api_env.py
        ;;
    2)
        echo ""
        echo "进入交互模式..."
        python3 web_search_api_env.py --interactive
        ;;
    *)
        echo "退出"
        exit 0
        ;;
esac

echo ""
echo "========================================"
echo "  执行完成"
echo "========================================"
