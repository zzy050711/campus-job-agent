import json


def get_jobs():

    with open("jobs.json", "r", encoding="utf-8") as f:
        jobs = json.load(f)

    return jobs
