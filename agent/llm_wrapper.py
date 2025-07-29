from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class LLMInference:
    def __init__(self, model_name: str = None,
                 device: str = "mps" if torch.backends.mps.is_available() else ("cuda" if torch.cuda.is_available() else "cpu")):
        """
        Initialize the LLM Inference wrapper.
        :param model_name: HuggingFace model repo to load
        :param device: Device to load the model on (default: mps if available, else cuda or cpu)
        """
        self.model = None
        self.tokenizer = None
        self.device = device
        
        if not model_name:
            print("No model name provided, using default model.")
            model_name = "deepseek-ai/deepseek-coder-1.3b-instruct"

        self.model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16, device_map="auto")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

    def inference(self, messages: dict, max_tokens: int = 1024, temperature: float = 0.0) -> str:
        """
        Generate a response from chat-style messages using apply_chat_template.
        :param messages: List of dicts with role/content format (chat style)
        :param max_tokens: Max new tokens to generate
        :param temperature: Sampling temperature (0.0 = deterministic)
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
            eos_token_id=self.tokenizer.eos_token_id,
            pad_token_id=self.tokenizer.eos_token_id,
        )

        decoded = self.tokenizer.decode(
            outputs[0][len(inputs[0]):], # Remove prompt tokens
            skip_special_tokens=True
        )

        return decoded
