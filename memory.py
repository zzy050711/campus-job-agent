import json
import os


MEMORY_FILE = "memory.json"


def load_memory():

    if not os.path.exists(MEMORY_FILE):
        return {
            "name": None,
            "skills": [],
            "target_job": None,
            "education": None,
            "projects": [],
            "advantages": [],
            "weaknesses": [],
            "suggestions": [],
            "conversation_history": []
        }

    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 兼容旧版本 memory.json
    data.setdefault("name", None)
    data.setdefault("skills", [])
    data.setdefault("target_job", None)
    data.setdefault("education", None)
    data.setdefault("projects", [])
    data.setdefault("advantages", [])
    data.setdefault("weaknesses", [])
    data.setdefault("suggestions", [])
    data.setdefault("conversation_history", [])

    return data


memory = load_memory()


def save_memory(
    name=None,
    skills=None,
    target_job=None
):

    if name:
        memory["name"] = name

    if skills:
        memory["skills"] = skills

    if target_job:
        memory["target_job"] = target_job

    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(
            memory,
            f,
            ensure_ascii=False,
            indent=4
        )


def save_resume_analysis(resume_data):

    if resume_data.get("name"):
        memory["name"] = resume_data["name"]

    if resume_data.get("skills"):
        memory["skills"] = resume_data["skills"]

    if resume_data.get("education"):
        memory["education"] = resume_data["education"]

    if resume_data.get("projects"):
        memory["projects"] = resume_data["projects"]

    if resume_data.get("advantages"):
        memory["advantages"] = resume_data["advantages"]

    if resume_data.get("weaknesses"):
        memory["weaknesses"] = resume_data["weaknesses"]

    if resume_data.get("suggestions"):
        memory["suggestions"] = resume_data["suggestions"]

    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(
            memory,
            f,
            ensure_ascii=False,
            indent=4
        )


def get_memory():
    return memory


def get_user_profile():

    return {
        "name": memory["name"],
        "skills": memory["skills"],
        "target_job": memory["target_job"],
        "education": memory["education"],
        "projects": memory["projects"],
        "advantages": memory["advantages"],
        "weaknesses": memory["weaknesses"],
        "suggestions": memory["suggestions"]
    }


def save_conversation(
    user_message,
    assistant_message
):

    memory["conversation_history"].append({
        "user": user_message,
        "assistant": assistant_message
    })

    memory["conversation_history"] = (
        memory["conversation_history"][-10:]
    )

    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(
            memory,
            f,
            ensure_ascii=False,
            indent=4
        )