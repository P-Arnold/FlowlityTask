#!/usr/bin/env sh

set -e

# build
npm run build

# navigate into the build output directory
cd dist

#Uncomment below to install serve
#npm install -g serve 

serve -s . -l 8080
