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

# Find common files in both directories
common_files=$(comm -12 <(cd "$dir1" && find . -type f -printf "%P\n" | sort) <(cd "$dir2" && find . -type f -printf "%P\n" | sort))

# Compare directories
diff -rq "$dir1" "$dir2" | grep 'Only'

# Initialize mismatch counter
mismatch_count=0

# Print header for the table
printf "%-40s | %-10s | %-10s | %s\n" "File" "Size (Dir1)" "Size (Dir2)" "Difference (KB)"
printf "%-40s-|-%-10s-|-%-10s-|-%s\n" "----------------------------------------" "----------" "----------" "-------------"

# Compare file sizes
while IFS= read -r file; do
  size1=$(du -k "${dir1}/${file}" | cut -f1)
  size2=$(du -k "${dir2}/${file}" | cut -f1)

  if [ "$size1" -ne "$size2" ]; then
    let "diff = size1 - size2"
    abs_diff=$(echo "$diff" | awk ' { if($1 >= 0) { print $1 } else { print $1 * -1 } } ')
    if [ "$abs_diff" -gt 4 ]; then #Here 3 is difference of 3KB, hence it will only show files with difference of more than 3 KB
      let "mismatch_count+=1"
      printf "%-40s | %-10d | %-10d | %d\n" "$file" "$size1" "$size2" "$diff"
    fi
  fi
done <<< "$common_files"

echo "Total number of mismatches: $mismatch_count"