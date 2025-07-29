import re

def extract_python_code_from_response(response: str) -> str:
    """
    Extracts Python code from the LLM response robustly using regex.
    Handles various formats like markdown code blocks and inline code.
    """
    # Case 1: Markdown-style Python block: ```python ... ```
    code_block = re.findall(r"```(?:python)?\s*([\s\S]*?)```", response, re.IGNORECASE)
    if code_block:
        return code_block[0].strip()

    # Case 2: Inline code assignment like result = { ... }
    inline_result = re.search(r"(result\s*=\s*{[\s\S]*?})", response)
    if inline_result:
        return inline_result.group(1).strip()

    # Case 3: Fallback – extract just a Python dict-looking string
    dict_like = re.search(r"({\s*['\"]classification['\"].*?['\"]explanation['\"].*?})", response, re.DOTALL | re.IGNORECASE)
    if dict_like:
        return f"result = {dict_like.group(1).strip()}"

    raise ValueError("No valid Python code or dictionary found in the response.")

def execute_result_code(code: str) -> dict:
    """
    Executes the extracted Python code and returns the `result` dictionary.
    Ensures safety by controlling the execution context.
    """
    local_vars = {}
    try:
        exec(code, {}, local_vars)
        result = local_vars.get("result", {})

        if isinstance(result, dict) and "classification" in result and "explanation" in result:
            return result
        else:
            raise ValueError("Missing expected keys in the result.")
    except Exception as e:
        print(f"[Execution Error] {e}")
        return {
            "classification": "Not Sure",
            "explanation": "Failed to parse or execute the LLM response properly."
        }
