#!/usr/bin/env python3
"""
联网搜索 API 调用脚本
基于 web_search.md 的 OpenAPI 规范创建
"""

import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

# ============== 配置区域 ==============
# API 配置
API_KEY = os.getenv("API_KEY", "")
BASE_URL = os.getenv("BASE_URL", "https://yunwu.ai")
API_ENDPOINT = f"{BASE_URL}/v1/messages"

# 模型配置
DEFAULT_MODEL = "claude-opus-4-6"
DEFAULT_MAX_TOKENS = 1024
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

    def _get_headers(self):
        """构建请求头"""
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

    def search(self, query, model=None, max_tokens=None, max_uses=5, stream=False):
        """
        执行联网搜索

        Args:
            query: 搜索查询内容
            model: 使用的模型名称，默认为 claude-sonnet-4-20250514
            max_tokens: 最大生成 token 数，默认为 1024
            max_uses: 搜索工具最大使用次数，默认为 5
            stream: 是否使用流式返回，默认为 False

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

            # 返回 JSON 结果
            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"API 请求错误: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"响应内容: {e.response.text}")
            raise

    def print_response(self, response):
        """
        格式化打印 API 响应

        Args:
            response: API 返回的响应字典
        """
        print("\n" + "="*60)
        print("API 响应结果")
        print("="*60)

        # 打印基本信息
        print(f"ID: {response.get('id', 'N/A')}")
        print(f"创建时间: {response.get('created', 'N/A')}")
        print(f"对象类型: {response.get('object', 'N/A')}")

        # 打印返回内容
        choices = response.get('choices', [])
        if choices:
            print(f"\n回复内容:")
            for idx, choice in enumerate(choices):
                message = choice.get('message', {})
                content = message.get('content', '')
                print(f"\n[选项 {idx}]:")
                print(content)
                print(f"结束原因: {choice.get('finish_reason', 'N/A')}")

        # 打印使用统计
        usage = response.get('usage', {})
        if usage:
            print(f"\nToken 使用统计:")
            print(f"  提示 Tokens: {usage.get('prompt_tokens', 0)}")
            print(f"  完成 Tokens: {usage.get('completion_tokens', 0)}")
            print(f"  总计 Tokens: {usage.get('total_tokens', 0)}")

        print("="*60 + "\n")


def main():
    """主函数 - 使用示例"""

    # 检查 API Key 是否已配置
    if API_KEY == "YOUR_API_KEY":
        print("⚠️  警告: 请先在脚本中配置您的 API_KEY")
        print("请修改脚本顶部的 API_KEY 变量")
        return

    # 创建 API 客户端
    client = WebSearchAPI()

    # 示例查询
    query = "What is the weather in NYC?"

    print(f"正在搜索: {query}")
    print(f"API 端点: {API_ENDPOINT}")

    try:
        # 执行搜索
        response = client.search(query)

        # 打印结果
        client.print_response(response)

        # 保存结果到文件（可选）
        with open('search_result.json', 'w', encoding='utf-8') as f:
            json.dump(response, f, ensure_ascii=False, indent=2)
        print("✓ 结果已保存到 search_result.json")

    except Exception as e:
        print(f"❌ 执行失败: {e}")


if __name__ == "__main__":
    main()
