import json
import re
def exact_match(output,expected):
    expected = expected.strip().lower()
    output = output.strip().lower()
    if expected in output: return 1
    return 0


def llm_as_a_judge(question, got, criteria, run_prompt_fn):
    judge_prompt = f"""
question: {question}
answer: {got}
criteria: {criteria}

Rate 1-10. Reply ONLY as JSON:
{{"score": X, "reason": "..."}}
"""

    result = run_prompt_fn(judge_prompt)

    print("Judge Response:")
    print(result.response)

    # Clean markdown code fences
    text = result.response
    text = re.sub(r"^```json\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    text = text.strip()

    return json.loads(text)