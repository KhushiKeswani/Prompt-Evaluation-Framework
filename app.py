from runner.promptrunner import PromptRunner
from evaluators.evaluate import evaluate
from classifier.intent_classifier import classify_task
runner = PromptRunner()
import json


TASK_METRIC_MAP = {
    "factual": "exact_match",
    "structured": "rubric",
    "open_ended": "llm_judge"
}
with open(r"C:\Users\DELL\prompt-engine\datasets\multiversion_prompts.json", "r") as file:
    data = json.load(file)
expected_data = []
for task in data:
    versions = task["versions"]
    first_prompt = versions[0]["prompt"]
    task_type = classify_task(first_prompt,runner.run)
    print(task_type)
    metric = TASK_METRIC_MAP[task_type]
    for version in task["versions"]:
        prompt = version["prompt"]
        version_id = version["id"]

        # use the SAME metric here
        task["task_type"] = task_type
        task["metric"] = metric
        case = {
    "id": version["id"],
    "input": version["prompt"],
    "metric": metric,
    "rules": [
    "valid_json",
    "no_markdown",
    "no_extra_text"]}
        expected_data.append(case)
print(expected_data)
results = evaluate(expected_data,runner.run)
print(results)

with open('datasets/enriched_data.json','r') as file:
    dataa = json.load(file)
with open("results/experiment_001.json","r") as file:
    resultdata = json.load(file)
all_result = resultdata
for case in dataa:
    exists = any(
    r["details"][0]["id"] == case["task_id"] and
    r["details"][0]["version"] == case["version_id"]
    for r in all_result)
    if exists:
        continue
    else:
        results = evaluate([case],runner.run)
        print(results)
        all_result.append(results)
        with open("results/experiment_001.json", "w") as f:
            json.dump(all_result, f, indent=4)

