import json
from runner.promptrunner import PromptRunner
runner = PromptRunner()
def classify_task(content, run_prompt_fn):
    # 1. Build classification prompt
    prompt = f"""
    You are a task classifier.

    Categories:
    - factual
    - structured
    - open_ended

    Content:
    {content}

    Reply with ONLY one category.
    """

    # 2. Send to LLM
    result = run_prompt_fn(prompt)

    # 3. Clean response
    category = result.response.lower().strip().strip('.')

    # 4. Validate category
    allowed = {"factual", "structured", "open_ended"}

    if category not in allowed:
        return None

    return category


    