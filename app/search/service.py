from search.llm import query_openrouter

def get_framework_recommendation(task_description: str) -> str:
    if not task_description.strip():
        return "Описание задачи пустое"
    result = query_openrouter(task_description)
    return result