from fastapi import FastAPI,UploadFile,File
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from services.resume_service import analyze_resume_file
from agent import agent
import os

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

    result = agent(request.question)

    return {
        "answer": result
    }

# 创建 /analyze_resume 接口
@app.post("/analyze_resume")
async def analyze_resume(
    file: UploadFile = File(...)
):

    result = analyze_resume_file(file)

    return result

# 创建 /download_resume 接口
@app.get("/download_resume")
def download_resume():
    return FileResponse(
        "AI定制简历.docx",
        filename="AI定制简历.docx",
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
