#!/bin/bash
# Usage: ./scripts/run_musescore.sh <input.mxl> <output.pdf>
# Example: ./scripts/run_musescore.sh \
#   tests/output/gariboldi-no1-alto.mxl tests/output/gariboldi-no1-alto.pdf

set -e

INPUT="${1:?Usage: $0 <input.mxl> <output.pdf>}"
OUTPUT="${2:?Usage: $0 <input.mxl> <output.pdf>}"

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

echo "Rendering: $INPUT -> $OUTPUT"

MSYS_NO_PATHCONV=1 docker compose run --rm musescore \
  "/data/$INPUT" \
  "/data/$OUTPUT"

echo "Done: $OUTPUT"
