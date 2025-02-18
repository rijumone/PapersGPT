#!/bin/bash

SESSION_NAME=$1
WORK_DIR=$2
ACTION=$3  # start or stop
CMD=".venv/bin/python -m streamlit run --server.port 8501 src/main.py"

cd "$WORK_DIR" || exit 1

if [ "$ACTION" == "stop" ]; then
    # Check if the tmux session exists
    if tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
        echo "Killing existing tmux session: $SESSION_NAME"
        tmux kill-session -t "$SESSION_NAME"
    fi
    exit 0
elif [ "$ACTION" == "start" ]; then
    # Check if the tmux session exists
    if tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
        echo "Tmux session $SESSION_NAME already started."
    else
        echo "Starting new tmux session: $SESSION_NAME"
        tmux new -d -s "$SESSION_NAME" "$CMD"
    fi
    exit 0
else
    echo "Invalid action. Use 'start' or 'stop'."
    exit 1
fi