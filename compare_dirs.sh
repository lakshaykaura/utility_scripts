#!/bin/bash

dir1="$1"
dir2="$2"

if [[ -z "$dir1" || -z "$dir2" ]]; then
  echo "Usage: $0 <directory1> <directory2>"
  exit 1
fi

if [[ ! -d "$dir1" || ! -d "$dir2" ]]; then
  echo "Both arguments must be directories."
  exit 1
fi

# Compare directories
diff -rq "$dir1" "$dir2" | grep 'Only'