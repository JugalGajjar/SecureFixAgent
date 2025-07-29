from agent.llm_wrapper import LLMInference
from agent.parse_response import extract_python_code_from_response, execute_result_code
from bandit_wrapper.run_bandit import run_bandit

def run_pipeline(code_file: str = "data/test_vuln.py", llm: LLMInference = None) -> dict:
    """
    Run the LLM inference pipeline with the given prompt and model.
    :param code_file: Path to the code file to analyze
    :param llm: LLMInference instance to use for generating responses
    :return: Parsed response from the LLM
    """
    if llm is None:
        llm = LLMInference()
    print("LLMInference instance created.")
    
    with open("prompts/system_classify_explain_template.txt", "r") as f:
        system_prompt = f.read().strip()
    print("System prompt loaded.")

    with open("prompts/user_input_template.txt", "r") as f:
        user_prompt = f.read().strip()
    print("User prompt loaded.")

    with open(code_file, "r") as f:
        code = f.read().strip()
    print(f"Code file '{code_file}' loaded.")
    
    bandit_report = str(run_bandit(code_file))
    print("Bandit report generated.")
    
    user_prompt = user_prompt.format(code_snippet=code, report=bandit_report)

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    response = llm.inference(messages)
    print("LLM response generated.")

    code = extract_python_code_from_response(response)
    print("Generated code:")
    print(response)

    parsed = execute_result_code(code)
    print("LLM response parsed.")

    return parsed


if __name__ == "__main__":
    model_name = "Qwen/Qwen2.5-Coder-3B-Instruct"

    llm = LLMInference(model_name=model_name, device="mps")

    output = run_pipeline("data/test_vuln2.py", llm)
    print("Parsed LLM output:")
    print("------------------")
    for key, value in output.items():
        print(f"{key}: {value}")