import json

from services.llm_service import chat_with_llm
from prompts.resume_generate_prompt import RESUME_GENERATE_PROMPT


def generate_resume_content(
        profile,
        target_job,
        job_requirement,
        resume_feedback
):

    prompt = RESUME_GENERATE_PROMPT.format(
        profile=json.dumps(
            profile,
            ensure_ascii=False,
            indent=2
        ),
        feedback=json.dumps(
            resume_feedback,
            ensure_ascii=False,
            indent=2
        ),
        target_job=target_job,

        job_requirement=job_requirement
    )


    response = chat_with_llm(
        [
            {
                "role":"user",
                "content":prompt
            }
        ]
    )


    content = response.choices[0].message.content


    return json.loads(content)