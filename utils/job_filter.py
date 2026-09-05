def filter_jobs(resume_text, jobs, target_job=None):

    matched_jobs = []

    resume_text = resume_text.lower()

    for job in jobs:

        matched_skills = []

        for skill in job["技能要求"]:

            if skill.lower() in resume_text:
                matched_skills.append(skill)

        if matched_skills:

            # 计算技能匹配度
            skill_score = (
                len(matched_skills)
                / len(job["技能要求"])
                * 100
            )

            # 计算目标岗位匹配加分
            target_score = 0

            if target_job:
                if target_job.lower() in job["岗位名称"].lower():
                    target_score = 20

            # 最终匹配度
            final_score = min(
                skill_score + target_score,
                100
            )

            job_result = {
                "岗位名称": job["岗位名称"],
                "公司": job["公司"],
                "技能要求": job["技能要求"],
                "已匹配技能": matched_skills,
                "技能匹配度": f"{skill_score:.0f}%",
                "目标岗位加分": target_score,
                "匹配度": f"{final_score:.0f}%"
            }

            matched_jobs.append(job_result)

    matched_jobs.sort(
        key=lambda x: int(
            x["匹配度"].replace("%", "")
        ),
        reverse=True
    )

    return matched_jobs