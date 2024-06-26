#!/bin/bash
export PYTHONPATH="/mnt/llm/home/ibragim-bad/code/SWE-bench"

python /mnt/llm/home/ibragim-bad/code/SWE-bench/swebench/harness/engine_validation.py \
    --instances_path "/mnt/llm/home/ibragim-bad/code/SWE-bench/data/versions/pydantic-task-instances_versions_versions.json" \
    --log_dir "/mnt/llm/home/ibragim-bad/code/SWE-bench/data/log_dir_2" \
    --temp_dir "/mnt/llm/home/ibragim-bad/code/SWE-bench/data/temp_dir" \
    --verbose \
    --path_conda "/mnt/llm/home/ibragim-bad/code/conda" 
    # --instance_id robotframework__robotframework-4722

# for file in $(ls /mnt/llm/home/ibragim-bad/code/SWE-bench/data/versions/*instances_versions.json); do
#     echo "$file"
#     python /mnt/llm/home/ibragim-bad/code/SWE-bench/swebench/harness/engine_validation.py \
#     --instances_path "$file" \
#     --log_dir "/mnt/llm/home/ibragim-bad/code/SWE-bench/data/log_dir" \
#     --temp_dir "/mnt/llm/home/ibragim-bad/code/SWE-bench/data/temp_dir" \
#     --verbose \
#     --path_conda "/mnt/llm/home/ibragim-bad/code/conda" \
#     --num_workers 1

# done