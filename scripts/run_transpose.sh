#!/bin/bash
# Usage: ./scripts/run_transpose.sh <input.mxl> <source_instrument> <target_instrument> <output.mxl>
# Example: ./scripts/run_transpose.sh \
#   tests/output/gariboldi-no1.mxl flute alto_sax tests/output/gariboldi-no1-alto.mxl

set -e

INPUT="${1:?Usage: $0 <input.mxl> <source> <target> <output.mxl>}"
SOURCE="${2:?Missing source instrument}"
TARGET="${3:?Missing target instrument}"
OUTPUT="${4:?Missing output path}"

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

MSYS_NO_PATHCONV=1 docker compose run --rm pipeline \
  "/data/$INPUT" \
  "$SOURCE" \
  "$TARGET" \
  "/data/$OUTPUT"
