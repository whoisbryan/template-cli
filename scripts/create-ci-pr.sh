#!/bin/bash

service_name=$1

cd tmp/repos/$service_name/
git pull origin main

git checkout -b 'feature/added-ci-files'
git add .
git commit -m "ci(pipeline): added files to create CI"
git status
git push --set-upstream origin feature/added-ci-files

gh pr create --title 'Added CI Files' --body 'SRE CLI 🎯 '
gh pr create --web