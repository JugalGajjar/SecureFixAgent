import os

from agent.llm_wrapper import LLMInference
from agent.parse_response import extract_python_code_from_phase1_response, execute_phase1_code
from agent.parse_response import extract_patch_from_phase2_response, execute_phase2_code
from bandit_wrapper.run_bandit import run_bandit

def run_pipeline(code_file: str = "data/vulnerable/test_vuln.py", llm: LLMInference = None) -> list:
    """
    Run the LLM inference pipeline with the given prompt and model.
    :param code_file: Path to the code file to analyze
    :param llm: LLMInference instance to use for generating responses
    :return: Parsed response from the LLM
    """
    if llm is None:
        llm = LLMInference()
    
    with open("prompts/system_classify_explain_template.txt", "r") as f:
        system_classify_explain_prompt = f.read().strip()
    with open("prompts/system_patch_template.txt", "r") as f:
        system_patch_prompt = f.read().strip()

    with open("prompts/user_classify_explain_template.txt", "r") as f:
        user_classify_explain_prompt = f.read().strip()
    with open("prompts/user_patch_template.txt", "r") as f:
        user_patch_prompt = f.read().strip()

    with open(code_file, "r") as f:
        code = f.read().strip()
    
    bandit_report = run_bandit(code_file)

    results = []

    for i, issue in enumerate(bandit_report):
        issue_prompt = user_classify_explain_prompt.format(code_snippet=code, report=str(issue))
        
        messages = [
            {"role": "system", "content": system_classify_explain_prompt},
            {"role": "user", "content": issue_prompt}
        ]

        response = llm.inference(messages)

        code = extract_python_code_from_phase1_response(response)
        parsed = execute_phase1_code(code)

        patch_prompt = user_patch_prompt.format(original_code=code, bandit_report_instance=str(issue), llm_response=parsed)

        messages = [
            {"role": "system", "content": system_patch_prompt},
            {"role": "user", "content": patch_prompt}
        ]

        response = llm.inference(messages)

        code = extract_patch_from_phase2_response(response)
        parsed = execute_phase2_code(code)

        results.append(parsed)
    
    for i in range(len(results)):
        results[i]["original_code"] = results[i]["original_code"].strip().replace("\\\"", "\"")
        results[i]["fixed_code"] = results[i]["fixed_code"].strip().replace("\\\"", "\"")
    
    with open(f"data/fixed/{code_file.split('/')[-1]}", "w") as f:
        f.write(results[0]["fixed_code"])

    return results


if __name__ == "__main__":
    model_name = "Qwen/Qwen2.5-Coder-3B-Instruct"

    llm = LLMInference(model_name=model_name, device="mps")

    output = run_pipeline("data/vulnerable/test_vuln.py", llm)
    os.system("clear")
    print(output[0]["original_code"])
    print("-" * 80)
    print(output[0]["fixed_code"])
    print("-" * 80)
    print(output[0]["why_safe"])