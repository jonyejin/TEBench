#!/bin/bash

cd ~/TEBench
git submodule update --remote --merge
git add .
git commit -m "Update submodules to latest commit"
git push origin main
