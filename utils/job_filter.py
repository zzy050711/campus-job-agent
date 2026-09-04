def filter_jobs(resume_text, jobs):

    matched_jobs = []

    resume_text = resume_text.lower()

    for job in jobs:

        matched_skills = []

        for skill in job["技能要求"]:

            if skill.lower() in resume_text:
                matched_skills.append(skill)

        if matched_skills:

            job_result = {
                "岗位名称": job["岗位名称"],
                "公司": job["公司"],
                "技能要求": job["技能要求"],
                "已匹配技能": matched_skills,
                "匹配度": f"{len(matched_skills) / len(job['技能要求']) * 100:.0f}%"
            }

            matched_jobs.append(job_result)

    matched_jobs.sort(
        key=lambda x: int(x["匹配度"].replace("%", "")),
        reverse=True
    )

    return matched_jobs