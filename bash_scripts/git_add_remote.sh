#!/usr/bin/env bash
#Check that arguments have been passed in
: "${1:?'Requires url link argument! Exiting..'}"

REPO_URL=$1

git add .
git commit -m "first commit"
git branch -M master
git remote add origin "${REPO_URL}"
git push -u origin master