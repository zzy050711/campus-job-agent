import json

from services.llm_service import chat_with_llm


def analyze_jd(jd_text):

    prompt = f"""
你是一名专业的招聘专家。

请分析下面的岗位JD：

{jd_text}

提取：

1. 岗位名称
2. 核心技能要求
3. 岗位职责
4. 经验要求

严格返回JSON：

{{
    "岗位名称": "",
    "技能要求": [],
    "岗位职责": [],
    "经验要求": ""
}}

不要输出JSON以外的内容。
"""

    response = chat_with_llm([
        {
            "role": "user",
            "content": prompt
        }
    ])
def match_resume_jd(resume_text, jd_text):

    prompt = f"""
你是一名校园招聘专家。

请比较学生简历和岗位JD。

学生简历：

{resume_text}


岗位JD：

{jd_text}


请分析：

1. 总体匹配度
2. 已具备技能
3. 技能缺口
4. 项目经历匹配情况
5. 简历优化建议


严格返回JSON：

{{
    "匹配度": "",
    "已具备技能": [],
    "技能缺口": [],
    "项目匹配": [],
    "简历优化建议": []
}}

不要编造学生不存在的经历。

不要输出JSON以外的内容。
"""

    response = chat_with_llm([
        {
            "role": "user",
            "content": prompt
        }
    ])

    content = response.choices[0].message.content

    return json.loads(content)