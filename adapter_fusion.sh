#!/bin/bash

# VARIABLES
MODEL="Qwen/Qwen2.5-Coder-3B-Instruct"
ADAPTER_PATH="qwen_3b_classify_explain_adapters"
SAVE_DIR="./qwen_3b_classify_explain_model"

# COMMAND
python -m mlx_lm.fuse \
    --model "$MODEL" \
    --save-path "$SAVE_DIR" \
    --adapter-path "$ADAPTER_PATH"