# 联网搜索 API 使用说明

## 快速开始

### 1. 安装依赖

```bash
pip install requests
```

如果需要使用环境变量配置（推荐），还需要安装：

```bash
pip install python-dotenv
```

### 2. 配置 API Key

#### 方法一：直接修改脚本（简单但不安全）

编辑 `web_search_api.py`，修改第 10 行：

```python
API_KEY = "your_actual_api_key_here"
```

#### 方法二：使用环境变量文件（推荐）

1. 复制 `.env.example` 为 `.env`：
   ```bash
   copy .env.example .env
   ```

2. 编辑 `.env` 文件，填入您的 API Key：
   ```
   API_KEY=sk-xxxxxxxxxxxxxxxxxxxxx
   ```

3. 修改 `web_search_api.py` 使其读取 `.env` 文件（需要安装 python-dotenv）

### 3. 运行脚本

```bash
python web_search_api.py
```

## API 信息

- **API 端点**: `https://yunwu.ai/v1/messages`
- **方法**: POST
- **认证**: Bearer Token
- **模型**: claude-sonnet-4-20250514

## 使用示例

### 基本使用

```python
from web_search_api import WebSearchAPI

# 创建客户端
client = WebSearchAPI(api_key="your_api_key")

# 执行搜索
response = client.search("What is the weather in NYC?")

# 打印结果
client.print_response(response)
```

### 自定义参数

```python
# 自定义模型和 token 数量
response = client.search(
    query="最新的 AI 技术发展",
    model="claude-sonnet-4-20250514",
    max_tokens=2048,
    max_uses=10  # 搜索工具最大使用次数
)
```

### 批量查询

```python
queries = [
    "Python 最佳实践",
    "机器学习入门教程",
    "云计算最新趋势"
]

for query in queries:
    print(f"\n搜索: {query}")
    response = client.search(query)
    client.print_response(response)
```

## 请求参数说明

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| query | string | 是 | 搜索查询内容 |
| model | string | 否 | 模型名称，默认 claude-sonnet-4-20250514 |
| max_tokens | integer | 否 | 最大生成 token 数，默认 1024 |
| max_uses | integer | 否 | 搜索工具最大使用次数，默认 5 |
| stream | boolean | 否 | 是否使用流式返回，默认 False |

## 响应格式

```json
{
  "id": "chatcmpl-123",
  "object": "chat.completion",
  "created": 1677652288,
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "搜索结果内容..."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 9,
    "completion_tokens": 12,
    "total_tokens": 21
  }
}
```

## 注意事项

1. **安全性**: 不要将 API Key 提交到版本控制系统（Git）
   - 将 `.env` 添加到 `.gitignore`
   - 使用环境变量或密钥管理服务

2. **错误处理**: 脚本已包含基本错误处理，会捕获并显示 API 错误

3. **超时设置**: 默认请求超时为 60 秒，可根据需要调整

4. **Token 限制**: 注意 API 的 token 使用限制和费用

## 故障排查

### 401 Unauthorized
- 检查 API Key 是否正确
- 确认 Authorization header 格式：`Bearer YOUR_API_KEY`

### 404 Not Found
- 确认 API 端点 URL 是否正确
- 检查 BASE_URL 配置

### 超时错误
- 增加 timeout 参数值
- 检查网络连接

### JSON 解析错误
- 检查 API 返回的响应格式
- 查看完整的错误响应内容

## 进阶使用

查看 `web_search.md` 了解完整的 OpenAPI 规范和所有可用参数。

## 相关文档

- [OpenAPI 规范](web_search.md)
- [官方文档](https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking)
