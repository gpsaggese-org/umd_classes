#!/bin/bash
# """
# Print version information for all installed packages.
#
# This script is useful for documenting the exact environment in which
# Docker containers are built and run.
# """

echo "=== Environment Information ==="
echo "Date: $(date)"
echo ""

echo "=== Python Version ==="
python --version

echo ""
echo "=== Key Packages ==="
pip list | grep -E "jupyter|pandas|numpy|pyarrow" || true

echo ""
echo "=== System Information ==="
uname -a

echo "=== Build Complete ==="
