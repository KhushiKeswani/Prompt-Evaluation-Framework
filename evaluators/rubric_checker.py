import json

def is_valid_json(text):
    try:
        import re
        output = re.sub(r"^```json\s*", "", text)
        output = re.sub(r"\s*```$", "", output)
        output = output.strip()
        return json.loads(output)
    except (json.JSONDecodeError, TypeError):
        return None

def no_markdown(text):
    return "```" not in text


def no_extra_text(text):
    import re

    cleaned = re.sub(r"^```json\s*", "", text)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    cleaned = cleaned.strip()

    try:
        obj = json.loads(cleaned)

        # Convert back to canonical JSON
        canonical = json.dumps(obj, separators=(",", ":"))

        # Normalize whitespace in original
        normalized = "".join(cleaned.split())

        return normalized == canonical

    except json.JSONDecodeError:
        return False

 
RULE_FUNCTIONS = {
    "no_markdown": no_markdown,
    "no_extra_text": no_extra_text,
}
 
 
def run_rubric(output: str, rules: list[str]) -> dict:
    """
    output: raw model response text
    rules: list of rule strings like ["valid_json", "has_key:summary", "under_words:50"]
    """
    results = {}
 
    # Step 1: valid_json always runs first, since everything else needs the parsed object
    parsed = is_valid_json(output)
    results["valid_json"] = parsed is not None
    if parsed is None:
        # can't check anything else meaningfully — short-circuit
        results["passed"] = False
        return results
 
    # Step 2: go through the remaining rules
    for rule in rules:
        if rule == "valid_json":
            continue  # already handled above
 
        if ":" in rule:
            name = rule.split(":", 1)
        else:
            name= rule, None
 
        fn = RULE_FUNCTIONS.get(name)
        if fn is None:
            results[rule] = False  # unknown rule name — fail safe
            continue
 
        if name == "no_markdwon":
            results[rule] = fn(parsed)
        elif name == "no_extra_text":
            # under_words checks the raw text length, not the parsed object
            results[rule] = fn(output)
        else:
            results[rule] = fn(parsed)
 
    results["passed"] = any(v for k, v in results.items() if k != "passed")
    return results
