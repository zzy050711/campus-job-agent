import json
import shutil

from utils.pdf_reader import read_pdf
from services.llm_service import chat_with_llm
from prompts.resume_prompt import RESUME_ANALYSIS_PROMPT
from services.job_service import get_jobs

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
    jobs = get_jobs()
    jobs_json = json.dumps(
    jobs,
    ensure_ascii=False,
    indent=2
)
    # 调用LLM
    response = chat_with_llm(
        [
            {
                "role": "system",
                "content":RESUME_ANALYSIS_PROMPT
            },
        {
    "role": "user",
    "content": f"""
下面是学生简历：

{resume_text}

下面是系统中的岗位：

{jobs_json}

请根据学生简历和岗位要求进行分析。
"""
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