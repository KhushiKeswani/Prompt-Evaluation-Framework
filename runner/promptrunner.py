from runner.model import PromptResult
import time
from llm.client import ask_ai
from evaluators.rubric_checker import run_rubric
class PromptRunner:

    def run(self,variable):
        start_time = time.perf_counter()
        print("API CALL")
        response,usage = ask_ai(variable)
        end_time = time.perf_counter()
        latency = end_time - start_time
        prompt_tokens = usage.prompt_token_count
        completion_tokens = usage.candidates_token_count
        total_tokens = usage.total_token_count
        result = PromptResult(
        prompt=variable,
        response=response,
        latency=latency,
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        total_tokens=total_tokens)

        return result
    