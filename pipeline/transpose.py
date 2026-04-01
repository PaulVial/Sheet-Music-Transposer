"""
Transpose a MusicXML file from one instrument to another.

Usage:
    python transpose.py <input.mxl> <source_instrument> <target_instrument> <output.mxl>

Example:
    python transpose.py score.mxl flute alto_saxophone transposed.mxl

Supported instruments: see INSTRUMENTS dict below.
"""

import sys
from music21 import converter, instrument, interval, stream, key

# Transposition intervals relative to concert pitch (C).
# Value = semitones that must be ADDED to concert pitch to get written pitch.
# e.g. alto saxophone sounds a major 6th lower than written, so +9 semitones written vs concert.
INSTRUMENTS = {
    "flute":            {"name": "Flute",            "semitones": 0},
    "oboe":             {"name": "Oboe",             "semitones": 0},
    "bassoon":          {"name": "Bassoon",          "semitones": 0},
    "piano":            {"name": "Piano",            "semitones": 0},
    "violin":           {"name": "Violin",           "semitones": 0},
    "clarinet_bb":      {"name": "Clarinet in Bb",   "semitones": 2},
    "trumpet_bb":       {"name": "Trumpet in Bb",    "semitones": 2},
    "soprano_sax":      {"name": "Soprano Saxophone","semitones": 2},
    "tenor_sax":        {"name": "Tenor Saxophone",  "semitones": 14},  # Bb + octave
    "alto_sax":         {"name": "Alto Saxophone",   "semitones": 9},
    "baritone_sax":     {"name": "Baritone Saxophone","semitones": 21}, # Eb + octave
    "french_horn":      {"name": "French Horn",      "semitones": 7},
    "clarinet_eb":      {"name": "Clarinet in Eb",   "semitones": -3},
}


def transpose_score(input_path: str, source_key: str, target_key: str, output_path: str) -> None:
    if source_key not in INSTRUMENTS:
        raise ValueError(f"Unknown source instrument '{source_key}'. Choose from: {list(INSTRUMENTS)}")
    if target_key not in INSTRUMENTS:
        raise ValueError(f"Unknown target instrument '{target_key}'. Choose from: {list(INSTRUMENTS)}")

    source = INSTRUMENTS[source_key]
    target = INSTRUMENTS[target_key]

    # Number of semitones to shift: bring to concert pitch, then write for target instrument
    semitones = target["semitones"] - source["semitones"]

    print(f"Source : {source['name']} ({source['semitones']:+d} semitones from concert)")
    print(f"Target : {target['name']} ({target['semitones']:+d} semitones from concert)")
    print(f"Transposing by {semitones:+d} semitones")

    score = converter.parse(input_path)

    transposition_interval = interval.Interval(semitones)
    transposed = score.transpose(transposition_interval)

    # Update key signatures throughout the score
    for ks in transposed.recurse().getElementsByClass(key.KeySignature):
        transposed_ks = ks.transpose(transposition_interval)
        ks.activeSite.replace(ks, transposed_ks)

    # Update instrument name in the score metadata
    for part in transposed.parts:
        part.partName = target["name"]
        for inst in part.recurse().getElementsByClass(instrument.Instrument):
            inst.partName = target["name"]

    transposed.write("musicxml", fp=output_path)
    print(f"Output written to {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print(__doc__)
        sys.exit(1)

    _, input_path, source_key, target_key, output_path = sys.argv
    transpose_score(input_path, source_key, target_key, output_path)
