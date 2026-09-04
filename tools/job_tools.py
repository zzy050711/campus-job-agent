from services.job_service import search_jobs, get_jobs
from utils.job_filter import filter_jobs

def search_jobs_tool(keyword: str):
    return search_jobs(keyword)

def match_jobs_tool(resume_text: str):
    jobs = get_jobs()

    return filter_jobs(
        resume_text,
        jobs
    )

def execute_tool(tool_name, arguments):

    if tool_name == "search_jobs":
        return search_jobs_tool(**arguments)

    if tool_name == "match_jobs":
        return match_jobs_tool(**arguments)

    return None