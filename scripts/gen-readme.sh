#!/bin/bash

echo "$(basename "$(pwd)")" > README.md
echo >> README.md

# There had best not be spaces in filenames...
for svg in $(ls *.svg|sort); do
    pdf="$(echo "${svg}"|sed -e 's/\.svg$/\.pdf/')"
    if [ ! -f "${pdf}" ]; then
        continue
    fi
    echo "## ${svg}" >> README.md
    echo >> README.md
    echo "![${svg}](${svg})" >> README.md
    echo >> README.md
    echo "[SVG](${svg}) | [PDF](${pdf})" >> README.md
    echo >> README.md
done
