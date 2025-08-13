#!/bin/bash

# VARIABLES
MODEL="Qwen/Qwen2.5-Coder-3B-Instruct"
DATA="./fine-tuning_data/classify_explain"
LR="4e-5"
ITERATIONS="200"
FINE_TUNE_TYPE="lora"
MAX_SEQ_LEN="4096"
NUM_LAYERS="6"

# COMMAND
python -m mlx_lm.lora \
    --model "$MODEL" \
    --train \
    --data "$DATA" \
    --learning-rate "$LR" \
    --iters "$ITERATIONS" \
    --num-layers "$NUM_LAYERS" \
    --fine-tune-type "$FINE_TUNE_TYPE" \
    --max-seq-length "$MAX_SEQ_LEN"