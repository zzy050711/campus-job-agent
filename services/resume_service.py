import json
import shutil

from utils.pdf_reader import read_pdf
from services.llm_service import chat_with_llm
from prompts.resume_prompt import RESUME_ANALYSIS_PROMPT
from services.job_service import get_jobs
from utils.job_filter import filter_jobs
from memory import save_resume_analysis


def analyze_resume_file(file):

    # 1. 保存上传文件
    file_path = f"temp_{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    # 2. 读取 PDF 文字
    resume_text = read_pdf(file_path)

    # 3. 获取系统岗位
    jobs = get_jobs()

    # 4. 根据简历进行岗位预筛选
    matched_jobs = filter_jobs(
        resume_text,
        jobs
    )

    jobs_json = json.dumps(
        matched_jobs,
        ensure_ascii=False,
        indent=2
    )

    # 5. 调用 LLM 分析简历
    response = chat_with_llm(
        [
            {
                "role": "system",
                "content": RESUME_ANALYSIS_PROMPT
            },
            {
                "role": "user",
                "content": f"""
下面是学生简历：

{resume_text}

下面是系统中与学生技能相关的岗位：

{jobs_json}

请根据学生简历和岗位要求进行分析。
"""
            }
        ]
    )

    # 6. 从 ChatCompletion 中取出真正的文本
    content = response.choices[0].message.content

    # 7. JSON 字符串转 Python 对象
    result = json.loads(content)

    # 8. 获取用户画像
    profile = result.get("用户画像", {})

    # 9. 整理成 Memory 需要的格式
    resume_memory = {
        "name": profile.get("姓名"),
        "skills": profile.get("技能", []),
        "education": profile.get("教育背景"),
        "projects": profile.get("项目经历", []),
        "advantages": profile.get("优势", []),
        "weaknesses": profile.get("不足", []),
        "suggestions": (
            result.get("简历优化建议", [])
            + result.get("学习规划", [])
        )
    }

    # 10. 保存到 Memory
    save_resume_analysis(resume_memory)

    # 11. 返回分析结果
    return result