from memory import get_user_profile

from services.doc_service import generate_resume

from services.resume_generator import generate_resume_content



def create_resume(
        target_job=None,
        job_requirement="",
        resume_feedback=None
):

    profile = get_user_profile()


    if not target_job:
        target_job = profile.get(
            "target_job"
        )


    resume_content = generate_resume_content(
        profile,
        target_job,
        job_requirement,
        resume_feedback
    )


    return generate_resume(
        resume_content
    )