#!/usr/bin/env sh

# abort on errors
set -e

# install, build
npm install
npm run build

# navigate into the build output directory
cd dist

#Uncomment line if serve not installed
#npm install -g serve
serve -s . -l 8080