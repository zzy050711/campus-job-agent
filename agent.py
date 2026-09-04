import json

from services.llm_service import chat_with_llm
from tools.job_tools import execute_tool
from memory import get_user_profile, save_memory, save_conversation


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
                    }
                },
                "required": ["resume_text"]
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

    # 4. 把用户画像交给 Agent
    messages = [
        {
            "role": "system",
            "content": f"""
你是一个校园求职 Agent。

这是你记住的用户信息：
{json.dumps(current_memory, ensure_ascii=False)}

请结合这些信息回答用户问题。

如果需要搜索岗位或匹配岗位，可以使用工具。
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
                    f"\n求职方向：{memory_data['target_job']}"
                )

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