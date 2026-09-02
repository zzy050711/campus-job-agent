import os
import json

from dotenv import load_dotenv
from openai import OpenAI


# 读取 .env
load_dotenv()

# 获取 API Key
api_key = os.getenv("DEEPSEEK_API_KEY")

# 创建 DeepSeek 客户端
client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)

# 调用大模型
user_input = input("请输入你的问题：")

response = client.chat.completions.create(
model="deepseek-v4-flash",
messages=[
    {
    "role": "system",
    "content": """
你是一名专业的校园求职顾问。

当用户询问求职问题时，请严格按照以下 JSON 格式回答：

{
    "适合岗位": ["岗位1", "岗位2", "岗位3"],
    "原因": "简要说明为什么适合",
    "技能缺口": ["技能1", "技能2", "技能3"],
    "建议": "给出具体的下一步建议"
}

不要输出 JSON 以外的任何内容。
"""
    },
    {
        "role": "user",
        "content": user_input
    }
    ]
)
# 打印 AI 回复
result = json.loads(response.choices[0].message.content)

print("适合岗位：", result["适合岗位"])
print("技能缺口：", result["技能缺口"])
print("建议：", result["建议"])