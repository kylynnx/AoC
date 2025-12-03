#!/usr/bin/env bash
base_dir="$(pwd)"

print_usage(){
  echo "Creates (empty) directory for new day.
    usage: $(basename "$0") <year> <day> [Optional: [-i/--input]]
      -i/--input: Create empty 'input.txt'

  "
}

if [ "$#" -lt 2 ]; then
  print_usage
  exit 1
fi

use_input="false"

if [ "$#" -gt 2 ]; then
  if ! ([ "$3" = "-i"  ] || [ "$3" = "--input" ]); then
    echo "Unknown argument: '$3'"
    print_usage
    exit 1
  else
    use_input="true"
  fi
fi

year="$1"
day="$2"

if [ ! -d "$year" ]; then
  echo "Creating new directory '$year'"
  mkdir $year
fi

cd $year

if [ -d "$day" ]; then
  echo "Directory $year/$day exists. Aborting."
  exit 1
fi

mkdir $day
cd $day
touch "exercise.md" "solution.py"

if [ "$use_input" = "true" ]; then
  touch "input.txt"
fi

git add ./
