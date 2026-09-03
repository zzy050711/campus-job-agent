import json
import shutil

from utils.pdf_reader import read_pdf
from services.llm_service import chat_with_llm


def analyze_resume_file(file):

    # 保存上传文件
    file_path = f"temp_{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )


    # 读取PDF文字
    resume_text = read_pdf(file_path)


    # 调用LLM
    response = chat_with_llm(
        [
            {
                "role": "system",
                "content": """
你是一名专业校园招聘顾问。

请分析下面这份学生简历。

返回JSON格式：

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


    # JSON字符串转对象
    result = json.loads(response)
    # 调用AI
    response = chat_with_llm(
    [
        {
            "role": "system",
            "content": """
            你是一名专业校园招聘顾问
            """
        },
        {
            "role": "user",
            "content": resume_text
        }
    ]
)

    return result