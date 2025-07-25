from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class LLMInference:
    def __init__(self, model_name="deepseek-ai/deepseek-coder-1.3b-instruct", device=None):
        """
        Initialize the LLM and tokenizer.
        :param model_name: HuggingFace model repo
        :param device: "mps" or "cuda" or "cpu", auto-detect if None
        """
        self.device = device or "mps" if torch.backends.mps.is_available() else ("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Loading model '{model_name}' on {self.device}")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name).to(self.device)

    def generate(self, messages, max_tokens=1024, temperature=0.0):
        """
        Generate a response from chat-style messages using apply_chat_template.
        :param messages: List of dicts with role/content format (chat style)
        :param max_tokens: Max new tokens to generate
        :param temperature: Sampling temperature (0 = deterministic)
        :return: Generated string
        """
        # Format chat template input
        try:
            inputs = self.tokenizer.apply_chat_template(
                messages,
                add_generation_prompt=True,
                return_tensors="pt"
            ).to(self.device)
        except Exception as e:
            raise ValueError(f"Failed to apply chat template: {e}")

        outputs = self.model.generate(
            inputs,
            max_new_tokens=max_tokens,
            do_sample=(temperature > 0),
            # temperature=temperature,
            eos_token_id=self.tokenizer.eos_token_id,
            pad_token_id=self.tokenizer.eos_token_id,
        )

        decoded = self.tokenizer.decode(
            outputs[0][len(inputs[0]):], # Remove prompt tokens
            skip_special_tokens=True
        )

        return decoded


if __name__ == "__main__":
    llm = LLMInference()
    prompt = "def add(a, b):\n    return a + b\n\n# Tell me what this function does."
    messages = [
        {"role": "user", "content": prompt}
    ]
    output = llm.generate(messages)
    print("LLM output:", output)
