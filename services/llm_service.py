from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)


def chat_with_llm(messages):

    response = client.chat.completions.create(
        model="deepseek-v4-flash",
        messages=messages
    )

    return response.choices[0].message.content