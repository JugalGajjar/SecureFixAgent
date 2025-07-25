# 🔐 SecureFixAgent

**Hybrid LLM Agents for Python Static Vulnerability Detection and Automated Repair**

---

## 📌 Overview

SecureFixAgent is a research-backed framework designed to improve Python code security by pairing lightweight, open-source LLMs with static analyzers like Bandit. The goal is to detect, explain, and automatically repair security vulnerabilities in Python programs — with reasoning, self-correction, and validation capabilities.

This hybrid approach combines the rule-based precision of static analyzers with the flexibility and generative power of code-specific LLMs to deliver high-quality, explainable fixes in a local, privacy-respecting environment.

---

## 🔄 Relation to Previous Work

SecureFixAgent builds upon our previously published research, [MalCodeAI](https://arxiv.org/abs/2507.10898), which explored leveraging large language models for malicious code detection and repair. While MalCodeAI focused primarily on classification and static patch generation using LLMs alone, SecureFixAgent introduces an agentic hybrid framework that combines static analysis (via Bandit) with LLM-based reasoning, re-validation, and iterative self-correction. This evolution addresses the limitations of purely LLM-based approaches and aims for more reliable, explainable, and automated security patching.

---

## 🎯 Research Goal

To enhance static vulnerability detection and automated repair in Python code by developing an intelligent LLM-based agent that:

- Collaborates with Bandit (static analyzer)
- Uses LLMs (≤8B parameters) for classification, explanation, and repair
- Employs an agentic loop with self-correction and re-validation
- Generalizes across synthetic and real-world Python repositories

---

## ❓ Research Questions

1. Can open-source LLMs (≤8B params) reliably detect, explain, and patch Python vulnerabilities when paired with static analyzers like Bandit?
2. Does an agentic loop featuring Bandit-based revalidation and iterative self-correction improve patch quality?
3. How do different LLMs (DeepSeek Coder, Qwen Coder, CodeGemma, etc.) compare on detection and repair performance?
4. Can this hybrid agent generalize to real-world Python codebases beyond controlled benchmarks?

---

## 🧠 LLM Agent Capabilities

- **Classification**: Categorizes issues as  `True Positive │ False Positive │ True Negative │ False Negative │ Not Sure`
- **Explanation**: Produces concise, CWE-style natural language descriptions
- **Fix Generation**: Applies secure patches to maintain functionality

---

## 🧱 System Architecture

```

   ┌──────────────┐
   │  Python Code │
   └──────────────┘
          │
          ▼
   ┌──────────────┐
   │  Bandit Scan │────────► Vulnerability Metadata
   └──────────────┘
          │
          ▼
   ┌──────────────────────────────┐
   │        LLM Agent Core        │
   ├──────────┬─────────┬─────────┤
   │ Classify │ Explain │   Fix   │
   └──────────┴─────────┴─────────┘
          │
          ▼
   ┌───────────────────────────────┐
   │ Re-run Bandit for validation? │
   └───────────────────────────────┘
          │
          ▼
   If issues remain ─► Retry Fix (max 5 iterations)

```

---

## 🛠️ Tools & Technologies

| Component          | Choice                                                                     |
| ------------------ | -------------------------------------------------------------------------- |
| Static Analyzer    | [Bandit](https://github.com/PyCQA/bandit)                                  |
| LLMs (≤8B)         | DeepSeek Coder 1.3B/6.7B, Qwen 2.5 Coder 3B/7B, CodeGemma 7B, CodeLlama 7B |
| Inference Backends | HuggingFace Transformers, Ollama, Apple MLX                                |
| Language           | Python                                                                     |
| Input Format       | Python source files or vulnerable code snippets                            |

---

## 🔁 Agentic Enhancements

### 1. **Re-Validation Decision**
After a patch is applied, the agent decides: _"Should we re-run Bandit to validate the fix?"_  
If **yes** → Bandit re-checks the modified code.

### 2. **Iterative Self-Correction**
If the issue persists:
- Agent re-prompts itself using the latest patch and updated Bandit report
- Attempts a new fix
- Loops until the fix is validated or 5 attempts are exhausted

---

## 📊 Evaluation Metrics

| Metric              | Description                                                      |
| ------------------- | ---------------------------------------------------------------- |
| Fix Accuracy        | % of vulnerabilities successfully fixed (Bandit no longer flags) |
| Precision           | Accuracy of classification (TP, FP, etc.)                        |
| Iteration Count     | Average number of patch attempts per fix                         |
| Explanation Quality | Subjective human rating on clarity and correctness               |

---

## 🙌 Acknowledgements

Inspired by advancements in static code analysis, lightweight LLMs, and open-source agentic workflows.