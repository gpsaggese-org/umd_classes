#!/bin/bash -e
START=$(date +%s)

#MODEL=llama3
#MODEL=mistral:7b-instruct-q4_K_M
#MODEL=phi3:mini
MODEL=tinyllama

echo $MODEL

llm -m $MODEL \
  "Explain recursion in 100 words" | tee output.txt

END=$(date +%s)
DURATION=$((END - START))

WORDS=$(wc -w < output.txt)

# Convert words → tokens (approx: 1 token ≈ 0.75 words)
TOKENS=$(awk "BEGIN {print $WORDS / 0.75}")

TPS=$(awk "BEGIN {print $TOKENS / $DURATION}")

echo "Duration: ${DURATION}s"
echo "Words: $WORDS"
echo "Estimated tokens: $TOKENS"
echo "Tokens/sec: $TPS"
