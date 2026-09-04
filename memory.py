import json
import os


MEMORY_FILE = "memory.json"


def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {
            "name": None,
            "skills": [],
            "target_job": None,
            "conversation_history": []
        }

    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


memory = load_memory()


def save_memory(name=None, skills=None, target_job=None):

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


def get_memory():
    return memory


def get_user_profile():
    return {
        "name": memory["name"],
        "skills": memory["skills"],
        "target_job": memory["target_job"]
    }

def save_conversation(user_message, assistant_message):

    memory["conversation_history"].append({
        "user": user_message,
        "assistant": assistant_message
    })

    # 只保留最近 10 轮
    memory["conversation_history"] = memory["conversation_history"][-10:]

    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(
            memory,
            f,
            ensure_ascii=False,
            indent=4
        )