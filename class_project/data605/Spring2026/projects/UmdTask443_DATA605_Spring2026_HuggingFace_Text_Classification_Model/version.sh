#!/bin/bash
# Report key package versions baked into this image.

echo "============================================================"
echo " Image version report — $(date -u '+%Y-%m-%d %H:%M UTC')"
echo "============================================================"
echo "Python   : $(python --version 2>&1)"
echo "pip      : $(pip --version 2>&1)"
echo "------------------------------------------------------------"

packages=(
    torch
    transformers
    datasets
    accelerate
    evaluate
    scikit-learn
    pandas
    numpy
    optuna
    jupyterlab
)

for pkg in "${packages[@]}"; do
    version=$(python -c "import importlib.metadata; print(importlib.metadata.version('$pkg'))" 2>/dev/null || echo "not installed")
    printf "%-20s %s\n" "$pkg" "$version"
done

echo "============================================================"
