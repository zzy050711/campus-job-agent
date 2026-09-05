from tools.job_tools import execute_tool


result = execute_tool(
    "get_memory",
    {}
)


print(result)