#!/bin/sh

run_python_script() {
    PYTHON_COMMAND="python3 main.py"
    $PYTHON_COMMAND
}

# Verifica se é meia-noite (00:00) para executar o script diariamente
if [ "$(date '+%H:%M')" = "00:00" ]; then
    run_python_script
fi