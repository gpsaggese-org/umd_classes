#!/bin/bash
# Fine-tune the transformer model inside Docker.
#   ./docker_train.sh                                  # DistilBERT default
#   ./docker_train.sh --model bert-base-uncased        # swap backbone
#   ./docker_train.sh --epochs 5 --batch_size 32       # override hyperparams
#   ./docker_train.sh --model roberta-base --lr 3e-5

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/docker_utils.sh"
load_docker_vars

CONTAINER_NAME="${IMAGE_NAME}_train"
# No -it so it can be run non-interactively (e.g. in CI or nohup).
OPTS=$(base_run_opts "$CONTAINER_NAME")

echo "🚀  Starting training — args: $*"
echo "    Fine-tuned model will be saved to ./models/ on your host."
echo ""

run "docker run $OPTS $FULL_IMAGE_NAME python project_files/scripts/train.py $*"

echo ""
echo "✅  Training complete. Check ./models/ for the saved checkpoint."
