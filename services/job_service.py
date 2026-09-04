import json


def get_jobs():
    return load_jobs_from_json()


def search_jobs(keyword=None):

    jobs = load_jobs_from_json()

    if not keyword:
        return jobs

    matched_jobs = []

    for job in jobs:

        text = (
            job["岗位名称"]
            + job["岗位描述"]
            + " ".join(job["技能要求"])
        )

        if keyword.lower() in text.lower():
            matched_jobs.append(job)

    return matched_jobs


def load_jobs_from_json():

    with open("jobs.json", "r", encoding="utf-8") as f:
        jobs = json.load(f)

    return jobs