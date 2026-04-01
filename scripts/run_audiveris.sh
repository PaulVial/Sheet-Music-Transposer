#!/bin/bash
# Usage: ./scripts/run_audiveris.sh <pdf_path>
# Example: ./scripts/run_audiveris.sh tests/perfect/gariboldi-thirty-easy-and-progressive-studies-no1.pdf

set -e

PDF_PATH="${1:?Usage: $0 <pdf_path>}"
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUTPUT_DIR="$REPO_ROOT/tests/output"

echo "Processing: $PDF_PATH"
echo "Output dir: $OUTPUT_DIR"

# cd to repo root so docker compose finds docker-compose.yml without -f
# MSYS_NO_PATHCONV=1 only affects the Linux paths passed as Audiveris arguments
cd "$REPO_ROOT"
MSYS_NO_PATHCONV=1 docker compose run --rm audiveris \
  -export \
  -output /data/tests/output \
  "/data/$PDF_PATH"

echo ""
echo "Done. Output files:"
ls -la "$OUTPUT_DIR/"
