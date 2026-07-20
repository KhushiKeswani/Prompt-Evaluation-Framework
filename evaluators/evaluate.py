import json
import time
from evaluators.rubric_checker import run_rubric
from evaluators.metrics import llm_as_a_judge,exact_match
def evaluate_one(case,run_prompt_fn):
    result = run_prompt_fn(case["input"])
    if case["metric"] == "exact_match":
        judge = llm_as_a_judge(
        question=case["input"],
        got=result.response,
        criteria="Answer must be factually correct, directly answer the question, and be concise.",
        run_prompt_fn=run_prompt_fn
    )

        return {
        "id": case["task_id"],
        "version": case["version_id"],
        "score": judge["score"] / 10,
        "method": "llm_judge",
        "judge_reason": judge["reason"],
        "latency": result.latency,
        "total_tokens": result.total_tokens,
    }
    
    if(case['metric']=='rubric'):
        print(case["task_id"])
        print(repr(result.response))
        print("-" * 50)
        rubric = run_rubric(result.response,case['rules'])
        if not rubric['passed']:
            return {"id": case["task_id"],"version": case["version_id"], "score": 0.0, "method": "rubric_failed",'rubric_results': rubric,'latency':result.latency,'total_tokens':result.total_tokens}
        return {"id": case["task_id"],"version": case["version_id"], "score": 1.0, "method": "rubric_passed",'rubric_results': rubric, 'latency':result.latency,'total_tokens':result.total_tokens}
    
    if(case['metric']=='llm_judge'):
        print(case["task_id"])
        print(repr(result.response))
        print("-" * 50)
        llm_judge = llm_as_a_judge(case["input"], result.response, "factual and concise", run_prompt_fn)
        return {"id": case["task_id"],"version": case["version_id"], "score": llm_judge['score']/10, "method": "llm_judge","judge_reason": llm_judge["reason"], 'latency':result.latency,'total_tokens':result.total_tokens}
def evaluate(dataset, run_prompt_fn):
    results_list = []  # 1. Create a empty list to collect individual results
    
    for f in dataset:
        result = evaluate_one(f, run_prompt_fn)
        results_list.append(result)  # 2. Append each single dictionary here
        print("Waiting 25 seconds to respect API rate limits...")
        time.sleep(25) 
    # 3. Calculate averages using your collected list outside the loop
    avg_score = sum(r['score'] for r in results_list) / len(results_list)
    avg_latency = sum(r['latency'] for r in results_list) / len(results_list)
    
    return {"avg_score": avg_score, "avg_latency": avg_latency, "details": results_list}

