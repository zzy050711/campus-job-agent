from fastapi import FastAPI,UploadFile,File
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from services.resume_service import analyze_resume_file
from agent import agent

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
    # 返回给前端
    return result