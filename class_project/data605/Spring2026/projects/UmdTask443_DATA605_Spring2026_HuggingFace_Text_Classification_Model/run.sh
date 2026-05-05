#!/bin/bash

#   ./run.sh                                      # full pipeline, all defaults
#   ./run.sh --model roberta-base                 # swap backbone
#   ./run.sh --model bert-base-uncased --epochs 5
#   ./run.sh --text "Apple reports record sales"  # custom prediction text
#   ./run.sh --skip-build                         # skip image build step

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

SKIP_BUILD=0
TRAIN_ARGS=""
PREDICT_TEXT=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --skip-build)
            SKIP_BUILD=1
            shift
            ;;
        --text)
            PREDICT_TEXT="$2"
            shift 2
            ;;
        --model|--epochs|--batch_size|--lr)
            TRAIN_ARGS="$TRAIN_ARGS $1 $2"
            shift 2
            ;;
        *)
            echo "Unknown argument: $1"
            echo "Usage: ./run.sh [--skip-build] [--model <name>] [--epochs <n>] [--batch_size <n>] [--lr <rate>] [--text <article>]"
            exit 1
            ;;
    esac
done

step() {
    echo ""
    echo "════════════════════════════════════════════════"
    echo "  $1"
    echo "════════════════════════════════════════════════"
}

# Step 1: Build
if [[ $SKIP_BUILD -eq 0 ]]; then
    step "Step 1/4 — Building Docker image"
    bash "$SCRIPT_DIR/docker_build.sh"
else
    step "Step 1/4 — Skipping build (--skip-build)"
fi

# Step 2: Train
step "Step 3/4 — Training model"
bash "$SCRIPT_DIR/docker_train.sh" $TRAIN_ARGS

# Step 3: Predict
step "Step 4/4 — Running inference"
if [[ -n "$PREDICT_TEXT" ]]; then
    bash "$SCRIPT_DIR/docker_predict.sh" --text "$PREDICT_TEXT"
else
    bash "$SCRIPT_DIR/docker_predict.sh" --text "Apple reports record iPhone sales in Q3"
fi

echo ""
echo "Pipeline complete!!!!"