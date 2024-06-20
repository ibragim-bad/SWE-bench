


#!/bin/bash
export PYTHONPATH="/mnt/llm/home/ibragim-bad/code/SWE-bench"

python /mnt/llm/home/ibragim-bad/code/SWE-bench/swebench/harness/engine_validation.py \
    --instances_path "/mnt/llm/home/ibragim-bad/code/SWE-bench/data/versions/Minigrid-task-instances_versions.json" \
    --log_dir "/mnt/llm/home/ibragim-bad/code/SWE-bench/data/log_dir" \
    --temp_dir "/mnt/llm/home/ibragim-bad/code/SWE-bench/data/temp_dir" \
    --num_workers 1 \
    --verbose \
    --path_conda "/mnt/llm/home/ibragim-bad/code/conda"

# for file in /mnt/llm/home/ibragim-bad/code/SWE-bench/data/versions/*instances_versions.json; do
#     echo "$file"
#     python /mnt/llm/home/ibragim-bad/code/SWE-bench/swebench/harness/engine_validation.py \
#     --instances_path "$file" \
#     --log_dir "/mnt/llm/home/ibragim-bad/code/SWE-bench/data/log_dir" \
#     --temp_dir "/mnt/llm/home/ibragim-bad/code/SWE-bench/data/temp_dir" \
#     --num_workers 1 \
#     --verbose \
#     --path_conda "/mnt/llm/home/ibragim-bad/code/conda"

# done