# Sheet Music Transposer

Sheet Music Transposer is a tool that takes a PDF sheet music file and produces a transposed PDF for a different instrument. A musician uploads a PDF, selects the source instrument (e.g. flute in C, alto saxophone in Eb) and the target instrument (e.g. tenor saxophone in Bb, clarinet in Bb), and downloads a clean, correctly transposed PDF. The pipeline handles key signature recalculation, accidentals, and preserves musical markings such as dynamics, articulations, and slurs.

The current focus is on digitally-generated PDFs (exports from MuseScore, Finale, Sibelius, or similar notation software) and monophonic parts.

## Pipeline

```
PDF -> Audiveris (OMR) -> MusicXML -> music21 (transposition) -> MuseScore headless (render) -> PDF
```

## Prerequisites

- Docker Desktop (tested with Docker 29)
- Git Bash or WSL on Windows

No other local dependencies are required. All tools (Audiveris, music21, MuseScore) run inside Docker containers.

## Repository structure

```
Sheet-Music-Transposer/
├── audiveris/                  # Audiveris Docker build context
│   ├── Dockerfile
│   └── audiveris-5.10.2/       # Audiveris source
├── scripts/
│   └── run_audiveris.sh        # Run Audiveris on a PDF
├── tests/
│   ├── perfect/                # Clean digitally-generated PDFs for validation
│   ├── limit/                  # Edge case PDFs (scans, complex layouts)
│   └── output/                 # Generated files (MusicXML, OMR artifacts)
└── docker-compose.yml
```

## Setup

### 1. Download Audiveris

Download the latest Audiveris release source archive from:

https://github.com/Audiveris/audiveris/releases/latest

Extract the archive into the `audiveris/` folder so the structure looks like this:

```
audiveris/
├── Dockerfile
└── audiveris-5.x.x/
    └── audiveris-5.x.x/
        ├── build.gradle
        ├── gradlew
        └── ...
```

Then update the `COPY` path in [audiveris/Dockerfile](audiveris/Dockerfile) if the version number differs from the one already set.

### 2. Build the Audiveris Docker image

This step compiles Audiveris from source inside Docker. It requires an internet connection to download Gradle and Java dependencies. It runs once and takes approximately 5 to 10 minutes.

```bash
docker compose build audiveris
```

### 3. Run Audiveris on a PDF

```bash
bash scripts/run_audiveris.sh tests/perfect/gariboldi-thirty-easy-and-progressive-studies-no1.pdf
```

The output MusicXML file (`.mxl`) will be written to `tests/output/`.

## Status

| Step | Description | Status |
|------|-------------|--------|
| 0 | Environment setup | Done |
| 1 | Audiveris: PDF to MusicXML | Done |
| 2 | music21: transposition | In progress |
| 3 | MuseScore headless: MusicXML to PDF | Pending |
| 4 | End-to-end pipeline | Pending |

## Notes

- Tessdata (Tesseract language data for text recognition) is downloaded automatically by Audiveris on first run and cached in a Docker volume named `audiveris-data`. Text elements such as tempo markings may be missing until tessdata is available.
- On Windows with Git Bash, the `run_audiveris.sh` script sets `MSYS_NO_PATHCONV=1` to prevent path conversion issues when passing container-internal paths to Docker.
