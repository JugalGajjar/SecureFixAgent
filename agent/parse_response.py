import re
import json

def parse_llm_response(response_text):
    """
    Parses the LLM response to extract classification and explanation,
    supporting JSON-like blocks with case-insensitive keys.

    Parameters:
        response_text (str): Raw string returned by LLM.

    Returns:
        dict: {
            'classification': str,
            'explanation': str
        }
    """
    # Try to find JSON-like block using regex
    json_block_match = re.search(r'\{.*?\}', response_text, re.DOTALL)
    if json_block_match:
        try:
            cleaned_block = json_block_match.group(0)
            parsed = json.loads(cleaned_block)

            # Normalize keys to lowercase
            parsed_lower = {k.lower(): v for k, v in parsed.items()}

            return {
                "classification": parsed_lower.get("classification", "Not Sure"),
                "explanation": parsed_lower.get("explanation", "Explanation not found.")
            }
        except json.JSONDecodeError:
            pass

    # Fallback regex-based parsing (also case-insensitive)
    classification_match = re.search(r"(?i)classification\s*[:\-]\s*(.+)", response_text)
    explanation_match = re.search(r"(?i)explanation\s*[:\-]\s*(.+)", response_text, re.DOTALL)

    classification = classification_match.group(1).strip() if classification_match else "Not Sure"
    explanation = explanation_match.group(1).strip() if explanation_match else "Explanation not found."

    return {
        "classification": classification,
        "explanation": explanation
    }

if __name__ == "__main__":
    sample_response = """
    Hello, I am an AI assistant.
    {
        "CLASSIFICATION": "False Positive",
        "explanation": "The subprocess input is hardcoded.\\nTherefore, it's a false positive. Related CWE: CWE-78."
    }
    Thank you!
    """

    result = parse_llm_response(sample_response)
    print(result)
