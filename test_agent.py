from agent import agent


question = """
这是一个AI应用开发工程师岗位JD：

岗位职责：
1. 负责大模型应用开发
2. 开发Agent智能体系统
3. 搭建RAG知识库问答系统


技能要求：
Python
FastAPI
LLM
RAG
Agent
LangChain


请根据我的情况分析匹配度，
然后帮我生成一份针对该岗位的简历。
"""


result = agent(question)


print(result)