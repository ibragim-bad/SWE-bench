export PYTHONPATH="/mnt/llm/home/ibragim-bad/code/SWE-bench"

# python /mnt/llm/home/ibragim-bad/code/SWE-bench/swebench/versioning/get_versions.py \
#     --instances_path "/mnt/llm/home/ibragim-bad/code/SWE-bench/data/microk8s-task-instances.jsonl" \
#     --retrieval_method build \
#     --conda_env "swe-bench" \
#     --num_workers 1 \
#     --path_conda "/mnt/llm/home/ibragim-bad/code/conda" \
#     --testbed "/mnt/llm/home/ibragim-bad/code/SWE-bench/data/testbed"

# Example call for getting versions from github web interface
# python get_versions.py \
#     --path_tasks "<path to sphinx task instances>" \
#     --retrieval_method github \
#     --num_workers 25 \
#     --output_dir "<path to folder to save versioned task instances to>"

#!/bin/bash

export PYTHONPATH="/mnt/llm/home/ibragim-bad/code/SWE-bench"

for file in /mnt/s3/llm/home/ibragim-bad/swebench/dump_tasks/*.jsonl; do
    echo "$file"
    python /mnt/llm/home/ibragim-bad/code/SWE-bench/swebench/versioning/get_versions.py \
        --instances_path "$file" \
        --retrieval_method build \
        --conda_env "swe-bench" \
        --num_workers 1 \
        --path_conda "/mnt/llm/home/ibragim-bad/code/conda" \
        --testbed "/mnt/llm/home/ibragim-bad/code/SWE-bench/data/testbed" \
        --output_dir "/mnt/llm/home/ibragim-bad/code/SWE-bench/data/versions"
done
