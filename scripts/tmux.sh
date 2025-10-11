#!/usr/bin/env bash

SESSION="tars"

tmux has-session -t "$SESSION" 2>/dev/null && tmux kill-session -t "$SESSION"

tmux new-session -d -s "$SESSION" -n main

tmux split-window -h -t "$SESSION":1
tmux split-window -v -t "$SESSION":1.1
tmux split-window -v -t "$SESSION":1.3
tmux split-window -v -t "$SESSION":1.4

tmux send-keys -t "$SESSION":1.1 "pnpm -F api docker:up && source ./apps/api/.venv/bin/activate && pnpm -F api dev" C-m
tmux send-keys -t "$SESSION":1.2 "pnpm -F web dev" C-m
tmux send-keys -t "$SESSION":1.3 "nvtop" C-m
tmux send-keys -t "$SESSION":1.4 "cd ~/llama.cpp/build/bin && ./llama-server -m ../../models/Qwen3-14B-Q6_K.gguf --port 8090 --jinja -ngl 35" C-m
tmux send-keys -t "$SESSION":1.5 "cd ~/llama.cpp/build/bin && ./llama-server -m ../../models/bge-large-en-v1.5_fp32.gguf --embedding --pooling cls -ub 8192 --port 9090" C-m

tmux attach-session -t "$SESSION"
