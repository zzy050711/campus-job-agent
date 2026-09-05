from services.job_service import search_jobs, get_jobs
from utils.job_filter import filter_jobs
from memory import get_user_profile
from tools.jd_tools import analyze_jd, match_resume_jd
from tools.resume_tools import create_resume
from tools.document_tools import parse_document

def execute_tool(name, args):


    if name == "search_jobs":

        return search_jobs(
            args["keyword"]
        )


    if name == "match_jobs":

        return filter_jobs(
            args["resume_text"],
            get_jobs(),
            args.get("target_job")
        )


    if name == "get_memory":

        return get_user_profile()

    if name == "create_resume":
        return create_resume(
        args.get("target_job")
    )
    if name == "analyze_jd":
        return analyze_jd(
            args["jd_text"]
        )

    if name == "match_resume_jd":
        return match_resume_jd(
            args["resume_text"],
            args["jd_text"]
        )

    if name == "parse_document":

        return parse_document(
        args["file_path"]
    )
    return {
        "error": "未知工具"
    }