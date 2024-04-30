#!/bin/bash

current_dir=$(basename "$(pwd)")
if [ "$current_dir" != "TEBench" ]; then
    echo "This script must be run from a TEBench directory."
    exit 1
fi

git submodule update --remote --merge
git add .
git commit -m "Update submodules to latest commit"
git push origin main
