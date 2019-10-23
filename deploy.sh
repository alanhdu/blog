#!/bin/sh

hugo
rm -rf ../alanhdu.github.io/*
mv public/* ../alanhdu.github.io

cd ../alanhdu.github.io
git reset HEAD^
git add .
git commit -m "Deploy"
git push -f origin master
