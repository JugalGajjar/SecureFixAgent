import os

from agent.llm_wrapper import LLMInference
from agent.parse_response import extract_python_code_from_phase1_response, execute_phase1_code
from agent.parse_response import extract_patch_from_phase2_response, execute_phase2_code
from bandit_wrapper.run_bandit import run_bandit

def run_pipeline(code_file: str = "data/vulnerable/test_vuln.py", llm1: LLMInference = None,  llm2: LLMInference = None) -> list:
    """
    Run the LLM inference pipeline with the given prompt and model.
    :param code_file: Path to the code file to analyze
    :param llm: LLMInference instance to use for generating responses
    :return: Parsed response from the LLM
    """
    if llm1 is None and llm2 is None:
        llm1 = llm2 = LLMInference()
    if llm1 is None:
        llm1 = llm2
    if llm2 is None:
        llm2 = llm1
    
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
        original_code = code
    
    bandit_report = run_bandit(code_file)

    results = []

    for i, issue in enumerate(bandit_report):
        issue_prompt = user_classify_explain_prompt.format(code_snippet=code, report=str(issue))
        
        messages = [
            {"role": "system", "content": system_classify_explain_prompt},
            {"role": "user", "content": issue_prompt}
        ]

        response = llm1.inference(messages, max_tokens=1024)

        code = extract_python_code_from_phase1_response(response)
        parsed = execute_phase1_code(code)

        if i == 0:
            patch_prompt = user_patch_prompt.format(original_code=code, bandit_report_instance=str(issue), llm_response=parsed)
        else:
            patch_prompt = user_patch_prompt.format(original_code=results[i-1]["fixed_code"], bandit_report_instance=str(issue), llm_response=parsed)

        messages = [
            {"role": "system", "content": system_patch_prompt},
            {"role": "user", "content": patch_prompt}
        ]

        response = llm2.inference(messages, max_tokens=4096)

        code = extract_patch_from_phase2_response(response)
        parsed = execute_phase2_code(code)

        results.append(parsed)
    
    for i in range(len(results)):
        results[i]["original_code"] = original_code
        results[i]["fixed_code"] = results[i]["fixed_code"].strip().replace("\\\"", "\"")
    
    with open(f"data/fixed/{code_file.split('/')[-1]}", "w") as f:
        f.write(results[-1]["fixed_code"])

    return results


if __name__ == "__main__":
    model1_name = "Qwen/Qwen2.5-Coder-7B-Instruct"
    model2_name = "Qwen/Qwen2.5-Coder-7B-Instruct"

    llm1 = LLMInference(model_name=model1_name, device="mps")
    llm2 = LLMInference(model_name=model2_name, device="mps")

    output = run_pipeline("data/vulnerable/test_vuln2.py", llm1, llm2)
    os.system("clear")
    print(output[-1]["original_code"])
    print("-" * 80)
    print(output[-1]["fixed_code"])
    print("-" * 80)
    print(output[-1]["why_safe"])