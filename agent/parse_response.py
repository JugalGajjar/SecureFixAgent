import re
import json

def extract_python_code_from_phase1_response(response: str) -> str:
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
    
    print("[Warning] No valid Python code or dictionary found in the response.")
    return """result = {
    "classification": "Not Sure",
    "explanation": "Failed to parse or extract valid Python code from the LLM response.
    }"""

def execute_phase1_code(code: str) -> dict:
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

def escape_for_python_string(text: str) -> str:
    """
    Escapes special characters so the string can be safely inserted into a Python dictionary.
    """
    return text.replace("\\", "\\\\").replace('"', '\\"').replace("'", "\\'")

def extract_patch_from_phase2_response(response: str) -> str:
    """
    Extracts the patch dictionary from the LLM Phase 2 response robustly using regex.
    Handles markdown code blocks, inline assignments, and fallback dictionary detection.
    """
    # Case 1: Markdown-style Python block
    code_block = re.findall(r"```(?:python)?\s*([\s\S]*?)```", response, re.IGNORECASE)
    if code_block:
        return code_block[0].strip()

    # Case 2: Inline code assignment like result = { ... }
    inline_result = re.search(r"(result\s*=\s*{[\s\S]*?})", response)
    if inline_result:
        return inline_result.group(1).strip()

    # Case 3: Fallback – dictionary-like structure with all required keys
    dict_like = re.search(
        r"({[\s\S]*?'original_code'[\s\S]*?'fixed_code'[\s\S]*?'bandit_report'[\s\S]*?'classification_explanation'[\s\S]*?'why_safe'[\s\S]*?})",
        response,
        re.DOTALL | re.IGNORECASE
    )
    if dict_like:
        return f"result = {dict_like.group(1).strip()}"

    print("[Warning] No valid Python patch dictionary found in the response.")
    return """result = {
    "original_code": "",
    "fixed_code": "",
    "bandit_report": "",
    "classification_explanation": "",
    "why_safe": ""
}"""

def execute_phase2_code(code: str) -> dict:
    """
    Executes the extracted Python code from Phase 2 and returns the `result` dictionary.
    Adds auto-escaping to prevent syntax errors from breaking the pipeline.
    """
    local_vars = {}
    try:
        exec(code, {}, local_vars)
        result = local_vars.get("result", {})

        required_keys = ["original_code", "fixed_code", "bandit_report", "classification_explanation", "why_safe"]
        if all(k in result for k in required_keys):
            # Ensure all strings are escaped for safety
            for k in required_keys:
                if isinstance(result[k], str):
                    result[k] = escape_for_python_string(result[k])
            return result
        else:
            raise ValueError("Missing expected keys in the patch result.")
    except Exception as e:
        print(f"[Execution Error] {e}")
        return {
            "original_code": "",
            "fixed_code": "",
            "bandit_report": "",
            "classification_explanation": "",
            "why_safe": ""
        }
