#!/usr/bin/env python3
"""
联网搜索 API 调用脚本（支持环境变量配置）
基于 web_search.md 的 OpenAPI 规范创建
"""

import requests
import json
import os
from pathlib import Path

# 尝试加载 python-dotenv（如果已安装）
try:
    from dotenv import load_dotenv
    # 加载 .env 文件
    env_path = Path(__file__).parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
        print("✓ 已从 .env 文件加载配置")
    else:
        print("ℹ 未找到 .env 文件，使用默认配置")
except ImportError:
    print("ℹ 未安装 python-dotenv，使用脚本内配置")
    print("  提示: pip install python-dotenv 以支持 .env 文件")

# ============== 配置区域 ==============
# API 配置（优先使用环境变量）
API_KEY = os.getenv("API_KEY", "YOUR_API_KEY")
BASE_URL = os.getenv("BASE_URL", "https://yunwu.ai")
API_ENDPOINT = f"{BASE_URL}/v1/messages"

# 模型配置
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "claude-sonnet-4-20250514")
DEFAULT_MAX_TOKENS = int(os.getenv("DEFAULT_MAX_TOKENS", "1024"))
# =====================================


class WebSearchAPI:
    """联网搜索 API 客户端"""

    def __init__(self, api_key=None):
        """
        初始化 API 客户端

        Args:
            api_key: API 密钥，如果不提供则使用全局配置
        """
        self.api_key = api_key or API_KEY
        self.base_url = BASE_URL
        self.endpoint = API_ENDPOINT

        # 验证 API Key
        if self.api_key == "YOUR_API_KEY" or not self.api_key:
            raise ValueError(
                "未配置有效的 API Key!\n"
                "请通过以下方式之一配置:\n"
                "1. 创建 .env 文件并设置 API_KEY=your_key\n"
                "2. 设置环境变量 API_KEY\n"
                "3. 在脚本中直接修改 API_KEY 变量"
            )

    def _get_headers(self):
        """构建请求头"""
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

    def search(self, query, model=None, max_tokens=None, max_uses=5,
               temperature=None, stream=False, verbose=True):
        """
        执行联网搜索

        Args:
            query: 搜索查询内容
            model: 使用的模型名称，默认为 claude-sonnet-4-20250514
            max_tokens: 最大生成 token 数，默认为 1024
            max_uses: 搜索工具最大使用次数，默认为 5
            temperature: 采样温度 (0-2)，控制输出随机性
            stream: 是否使用流式返回，默认为 False
            verbose: 是否打印详细信息，默认为 True

        Returns:
            API 响应结果（字典格式）
        """
        # 构建请求体
        payload = {
            "model": model or DEFAULT_MODEL,
            "max_tokens": max_tokens or DEFAULT_MAX_TOKENS,
            "messages": [
                {
                    "role": "user",
                    "content": query
                }
            ],
            "tools": [
                {
                    "type": "web_search_20250305",
                    "name": "web_search",
                    "max_uses": max_uses
                }
            ],
            "tool_choice": {
                "type": "any"
            },
            "stream": stream
        }

        # 可选参数
        if temperature is not None:
            payload["temperature"] = temperature

        if verbose:
            print(f"\n📡 发送请求到: {self.endpoint}")
            print(f"🔍 查询内容: {query}")
            print(f"🤖 使用模型: {payload['model']}")

        try:
            # 发送 POST 请求
            response = requests.post(
                self.endpoint,
                headers=self._get_headers(),
                json=payload,
                timeout=60
            )

            # 检查响应状态
            response.raise_for_status()

            if verbose:
                print(f"✓ 请求成功 (状态码: {response.status_code})")

            # 返回 JSON 结果
            return response.json()

        except requests.exceptions.HTTPError as e:
            print(f"❌ HTTP 错误: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"响应状态码: {e.response.status_code}")
                print(f"响应内容: {e.response.text}")
            raise
        except requests.exceptions.ConnectionError as e:
            print(f"❌ 连接错误: 无法连接到 API 服务器")
            print(f"请检查网络连接和 API 地址: {self.endpoint}")
            raise
        except requests.exceptions.Timeout as e:
            print(f"❌ 请求超时: API 响应时间过长")
            raise
        except requests.exceptions.RequestException as e:
            print(f"❌ 请求错误: {e}")
            raise
        except json.JSONDecodeError as e:
            print(f"❌ JSON 解析错误: {e}")
            print(f"响应内容: {response.text[:500]}")
            raise

    def print_response(self, response):
        """
        格式化打印 API 响应

        Args:
            response: API 返回的响应字典
        """
        print("\n" + "="*60)
        print("📊 API 响应结果")
        print("="*60)

        # 打印基本信息
        print(f"🆔 ID: {response.get('id', 'N/A')}")
        print(f"⏰ 创建时间: {response.get('created', 'N/A')}")
        print(f"📦 对象类型: {response.get('object', 'N/A')}")

        # 打印返回内容
        choices = response.get('choices', [])
        if choices:
            print(f"\n💬 回复内容:")
            for idx, choice in enumerate(choices):
                message = choice.get('message', {})
                content = message.get('content', '')
                print(f"\n[选项 {idx}]:")
                print("-" * 60)
                print(content)
                print("-" * 60)
                print(f"🏁 结束原因: {choice.get('finish_reason', 'N/A')}")

        # 打印使用统计
        usage = response.get('usage', {})
        if usage:
            print(f"\n📈 Token 使用统计:")
            print(f"  ➤ 提示 Tokens: {usage.get('prompt_tokens', 0)}")
            print(f"  ➤ 完成 Tokens: {usage.get('completion_tokens', 0)}")
            print(f"  ➤ 总计 Tokens: {usage.get('total_tokens', 0)}")

        print("="*60 + "\n")

    def save_response(self, response, filename="search_result.json"):
        """
        保存响应到 JSON 文件

        Args:
            response: API 返回的响应字典
            filename: 保存的文件名
        """
        try:
            filepath = Path(__file__).parent / filename
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(response, f, ensure_ascii=False, indent=2)
            print(f"✓ 结果已保存到: {filepath}")
        except Exception as e:
            print(f"❌ 保存文件失败: {e}")


def interactive_mode():
    """交互式模式"""
    print("\n" + "="*60)
    print("🔍 联网搜索 API - 交互模式")
    print("="*60)
    print("输入 'quit' 或 'exit' 退出\n")

    try:
        client = WebSearchAPI()
    except ValueError as e:
        print(f"\n❌ {e}")
        return

    while True:
        try:
            query = input("\n请输入搜索查询: ").strip()

            if query.lower() in ['quit', 'exit', 'q']:
                print("👋 再见!")
                break

            if not query:
                print("⚠️  查询不能为空")
                continue

            # 执行搜索
            response = client.search(query)

            # 打印结果
            client.print_response(response)

            # 询问是否保存
            save = input("是否保存结果? (y/n): ").strip().lower()
            if save == 'y':
                filename = f"search_{response.get('id', 'result')}.json"
                client.save_response(response, filename)

        except KeyboardInterrupt:
            print("\n\n👋 已取消，再见!")
            break
        except Exception as e:
            print(f"\n❌ 发生错误: {e}")
            continue_choice = input("是否继续? (y/n): ").strip().lower()
            if continue_choice != 'y':
                break


def main():
    """主函数 - 使用示例"""

    print("\n" + "="*60)
    print("🔍 联网搜索 API 调用脚本")
    print("="*60)
    print(f"📍 API 端点: {API_ENDPOINT}")
    print(f"🤖 默认模型: {DEFAULT_MODEL}")
    print("="*60)

    # 检查是否要进入交互模式
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == '--interactive':
        interactive_mode()
        return

    try:
        # 创建 API 客户端
        client = WebSearchAPI()

        # 示例查询列表
        queries = [
            "What is the weather in NYC?",
            # "最新的人工智能发展趋势",
            # "Python 3.12 有哪些新特性"
        ]

        for i, query in enumerate(queries, 1):
            print(f"\n{'='*60}")
            print(f"查询 {i}/{len(queries)}")
            print(f"{'='*60}")

            # 执行搜索
            response = client.search(query)

            # 打印结果
            client.print_response(response)

            # 保存结果
            filename = f"search_result_{i}.json"
            client.save_response(response, filename)

            # 如果有多个查询，等待一下
            if i < len(queries):
                import time
                print("\n⏳ 等待 2 秒后执行下一个查询...")
                time.sleep(2)

        print("\n✅ 所有查询完成!")
        print("\n💡 提示: 运行 'python web_search_api_env.py --interactive' 进入交互模式")

    except ValueError as e:
        print(f"\n❌ 配置错误: {e}")
        print("\n📖 配置指南:")
        print("1. 复制 .env.example 为 .env")
        print("2. 编辑 .env 文件，填入您的 API_KEY")
        print("3. 重新运行此脚本")
    except Exception as e:
        print(f"\n❌ 执行失败: {e}")


if __name__ == "__main__":
    main()
