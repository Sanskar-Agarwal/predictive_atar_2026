#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd $DIR
# Pulling from origin
# echo "Pulling from remote branch to check for update"
# current_branch=$(git rev-parse --abbrev-ref HEAD)

# if [ "$current_branch" = "usage" ]; then
#     echo "Current branch is 'usage'."
#     echo "Stashing change"
#     git stash
#     echo "Clearing Stash"
#     git stash clear
#     echo "Moving to main" 
#     git checkout main
#     echo "Download the update" 
#     git pull origin main
#     git checkout usage
#     git merge main
# else
#     echo "Current branch is not 'usage'."
#     git stash
#     git checkout main
#     git pull origin main 
#     git checkout -B usage
# fi

python3 run.py