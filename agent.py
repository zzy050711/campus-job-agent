import json

from services.llm_service import chat_with_llm
from tools.job_tools import execute_tool
from memory import get_user_profile, get_memory,save_memory, save_conversation
from tools.document_tools import *

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_jobs",
            "description": "根据关键词搜索岗位",
            "parameters": {
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string",
                        "description": "岗位搜索关键词，例如 AI、Python、大数据"
                    }
                },
                "required": ["keyword"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "match_jobs",
            "description": "根据学生简历内容匹配合适的岗位",
            "parameters": {
                "type": "object",
                "properties": {
                    "resume_text": {
                        "type": "string",
                        "description": "学生的简历内容"
                    },
                    "target_job": {
                        "type": "string",
                        "description": "用户目标岗位"
                    }
                },
                "required": ["resume_text"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "get_memory",
            "description": "获取用户的个人求职画像，包括技能、目标岗位、项目经历等",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },

{
    "type": "function",
    "function": {
        "name": "create_resume",
        "description": "根据用户个人画像和目标岗位生成定制版Word简历",
        "parameters": {
            "type": "object",
            "properties": {
                "target_job": {
                    "type": "string",
                    "description": "用户希望申请的目标岗位，例如 AI应用开发工程师、Python后端开发工程师"
                },
                "resume_feedback": {
                    "type": "object",
                    "description": "简历匹配分析结果"
                }
            },
            "required": []
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "analyze_jd",
        "description": "分析岗位JD，提取岗位名称、技能要求、岗位职责和经验要求",
        "parameters": {
            "type": "object",
            "properties": {
                "jd_text": {
                    "type": "string",
                    "description": "完整的岗位JD文本"
                }
            },
            "required": ["jd_text"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "match_resume_jd",
        "description": "比较学生简历与岗位JD，分析匹配度、技能缺口和简历优化方向",
        "parameters": {
            "type": "object",
            "properties": {
                "resume_text": {
                    "type": "string",
                    "description": "学生简历内容"
                },
                "jd_text": {
                    "type": "string",
                    "description": "岗位JD内容"
                }
            },
            "required": ["resume_text", "jd_text"]
        }
    }
},
{
"type":"function",
"function":{
"name":"parse_document",
"description":"读取用户上传的PDF简历或者岗位文件",
"parameters":{
"type":"object",
"properties":{
"file_path":{
"type":"string"
}
},
"required":[
"file_path"
]
}
}
}
]


def extract_memory(user_input):

    prompt = f"""
请从下面用户的话中提取值得长期记住的求职信息。

用户：
{user_input}

只输出 JSON：

{{
    "name": null,
    "skills": [],
    "target_job": null
}}

如果没有相关信息，就保持 null 或空数组。
"""

    response = chat_with_llm([
        {
            "role": "user",
            "content": prompt
        }
    ])

    content = response.choices[0].message.content

    return json.loads(content)


def agent(user_input):

    # 1. 从用户输入中提取新的记忆
    memory_data = extract_memory(user_input)

    # 2. 保存新的记忆
    save_memory(
        name=memory_data.get("name"),
        skills=memory_data.get("skills"),
        target_job=memory_data.get("target_job")
    )

    # 3. 获取当前用户画像
    current_memory = get_user_profile()
    memory_data = get_memory()
    conversation_history = memory_data.get(
    "conversation_history",
    []
)

    # 4. 把用户画像交给 Agent
    messages = [
        {
            "role": "system",
            "content": f"""
你是一个校园求职 Agent。

如果用户提供文件路径或者上传文件：

首先调用 parse_document 获取文件内容。

不要直接假设文件内容。

这是用户的个人信息：

{json.dumps(current_memory, ensure_ascii=False)}

这是用户最近的对话历史：

{json.dumps(conversation_history, ensure_ascii=False)}

你的任务是帮助用户进行校园求职。

如果用户询问：
- 适合什么岗位
- 推荐岗位
- 岗位匹配
- 我的技能适合什么工作

应该优先使用 match_jobs 工具。

如果用户明确要求搜索某类岗位，
使用 search_jobs 工具。

如果用户提供岗位JD并要求分析岗位，
使用 analyze_jd 工具。

如果用户希望知道自己的简历是否适合某个岗位，
或者希望分析自己与岗位的匹配程度，
使用 match_resume_jd 工具。

如果用户希望针对某个岗位修改或生成简历，
应该先分析岗位要求，再结合用户画像生成定制简历。

如果用户要求生成、创建、制作Word简历，
使用 create_resume 工具。

如果用户明确指定了目标岗位，
把目标岗位传给 create_resume。

如果用户没有指定目标岗位，
使用用户 Memory 中已经保存的 target_job。

create_resume 工具成功后，
告诉用户简历已经生成，
并告诉用户可以通过 /download_resume 下载。

岗位匹配结果返回后，你需要进一步分析：

1. 哪个岗位最适合用户
2. 为什么适合
3. 用户已经具备哪些技能
4. 用户缺少哪些技能
5. 给出简短的求职建议

不要只把工具返回的数据原样复制给用户，
要结合用户的个人信息进行分析。

最终使用自然语言回答。
"""
        },
        {
            "role": "user",
            "content": user_input
        }
    ]

    # 5. Tool Calling 循环
    while True:

        response = chat_with_llm(
            messages,
            tools=TOOLS
        )

        message = response.choices[0].message

        # 6. LLM 不需要工具，直接返回最终答案
        if not message.tool_calls:

            save_conversation(
                user_input,
                message.content
            )

            return message.content

        # 7. 把 LLM 的工具调用请求加入对话
        messages.append(message)

        # 8. 执行工具
        for tool_call in message.tool_calls:

            tool_name = tool_call.function.name

            arguments = json.loads(
                tool_call.function.arguments
            )

            # 9. 如果是岗位匹配，自动使用 Memory 中的用户技能
            if tool_name == "match_jobs":

                memory_data = get_user_profile()

                arguments["resume_text"] = (
            f"技能：{', '.join(memory_data['skills'])}"
        )
            if tool_name == "create_resume":

                memory_data = get_user_profile()

                if not arguments.get("target_job"):
                    arguments["target_job"] = memory_data["target_job"]

            # 10. 执行工具
            result = execute_tool(
                tool_name,
                arguments
            )

            # 11. 把工具结果返回给 LLM
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(
                        result,
                        ensure_ascii=False
                    )
                }
            )