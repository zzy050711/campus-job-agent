import os

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
            "role": "user",
            "content": user_input
        }
    ]
)


# 打印 AI 回复
print(response.choices[0].message.content)