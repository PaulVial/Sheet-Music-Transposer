#!/bin/bash
# Usage: entrypoint.sh <input.mxl> <output.pdf>
set -e
INPUT="${1:?Usage: $0 <input.mxl> <output.pdf>}"
OUTPUT="${2:?Usage: $0 <input.mxl> <output.pdf>}"
exec mscore3 -platform offscreen -o "$OUTPUT" "$INPUT"
