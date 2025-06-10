#!/bin/bash
# run_and_collect.sh — run all .py files and gather outputs

# Temporary raw output file
> raw_output.txt

# Find and run every .py file (including subfolders)
find . -type f -name '*.py' | while read file; do
  echo "=== $file ===" >> raw_output.txt
  python3 "$file" >> raw_output.txt 2>&1
  echo "" >> raw_output.txt
done

echo "Raw output saved to raw_output.txt"
