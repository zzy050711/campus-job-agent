import os
import json
import shutil

from dotenv import load_dotenv
from openai import OpenAI
from fastapi import FastAPI,UploadFile,File
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from utils.pdf_reader import read_pdf

# 读取 .env
load_dotenv()

# 获取 API Key
api_key = os.getenv("DEEPSEEK_API_KEY")

# 创建 DeepSeek 客户端
client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)

# 创建 FastAPI 应用
app = FastAPI()
@app.get("/")
def home():
    return FileResponse("index.html")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# 定义用户输入的数据格式
class UserRequest(BaseModel):
    question: str


# 创建 /analyze 接口
@app.post("/analyze")
def analyze(request: UserRequest):

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
                "content": request.question
            }
        ]
    )
# 创建 /analyze_resume 接口
@app.post("/analyze_resume")
async def analyze_resume(
        file: UploadFile = File(...)
):

    # 保存上传文件
    file_path = f"temp_{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )


    # 读取PDF文字
    resume_text = read_pdf(file_path)


    # 调用AI
    response = client.chat.completions.create(
        model="deepseek-v4-flash",
        messages=[
            {
                "role": "system",
                "content": """
你是一名专业校园招聘顾问。

分析学生简历，并返回JSON：

{
 "用户画像":"",
 "适合岗位":[],
 "技能缺口":[],
 "简历优化建议":"",
 "学习规划":""
}

不要输出其他内容。
"""
            },
            {
                "role": "user",
                "content": resume_text
            }
        ]
    )
    
    # AI 返回的是 JSON 字符串
    result = json.loads(response.choices[0].message.content)

    # 返回给前端
    return result