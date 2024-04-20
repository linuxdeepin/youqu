#!/bin/bash

pnpm run build
[ $? != 0 ] && exit 1

git clone git@github.com:linuxdeepin/youqu.git -b gh-pages gh-pages

cp -r --force docs/.vitepress/dist/* gh-pages/

cd gh-pages
git add .
git commit -m "docs deploy"
git push

cd ..
rm -rf gh-pages