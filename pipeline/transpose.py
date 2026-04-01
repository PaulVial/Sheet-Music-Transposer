"""
Transpose a MusicXML file from one instrument to another.

Usage:
    python transpose.py <input.mxl> <source_instrument> <target_instrument> <output.mxl>

Example:
    python transpose.py score.mxl flute alto_saxophone transposed.mxl

Supported instruments: see INSTRUMENTS dict below.
"""

import sys
from music21 import converter, dynamics, instrument, interval, layout, metadata, note, stream, key, text

# Transposition intervals relative to concert pitch (C).
# semitones = added to concert pitch to get written pitch.
# midi_min / midi_max = practical written range (MIDI note numbers).
INSTRUMENTS = {
    "flute":            {"name": "Flute",             "semitones": 0,  "midi_min": 60, "midi_max": 98},
    "oboe":             {"name": "Oboe",              "semitones": 0,  "midi_min": 58, "midi_max": 91},
    "bassoon":          {"name": "Bassoon",           "semitones": 0,  "midi_min": 34, "midi_max": 75},
    "piano":            {"name": "Piano",             "semitones": 0,  "midi_min": 21, "midi_max": 108},
    "violin":           {"name": "Violin",            "semitones": 0,  "midi_min": 55, "midi_max": 103},
    "clarinet_bb":      {"name": "Clarinet in Bb",    "semitones": 2,  "midi_min": 50, "midi_max": 91},
    "trumpet_bb":       {"name": "Trumpet in Bb",     "semitones": 2,  "midi_min": 52, "midi_max": 84},
    "soprano_sax":      {"name": "Soprano Saxophone", "semitones": 2,  "midi_min": 50, "midi_max": 87},
    "tenor_sax":        {"name": "Tenor Saxophone",   "semitones": 14, "midi_min": 50, "midi_max": 87},
    "alto_sax":         {"name": "Alto Saxophone",    "semitones": 9,  "midi_min": 46, "midi_max": 87},
    "baritone_sax":     {"name": "Baritone Saxophone","semitones": 21, "midi_min": 46, "midi_max": 87},
    "french_horn":      {"name": "French Horn",       "semitones": 7,  "midi_min": 40, "midi_max": 77},
    "clarinet_eb":      {"name": "Clarinet in Eb",    "semitones": -3, "midi_min": 50, "midi_max": 91},
}


def fit_to_range(transposed_score: stream.Score, target: dict) -> int:
    """Shift notes that fall outside the target instrument range by octaves."""
    midi_min = target["midi_min"]
    midi_max = target["midi_max"]
    adjusted = 0

    for n in transposed_score.recurse().getElementsByClass(note.Note):
        midi = n.pitch.midi
        if midi > midi_max:
            octaves = -((midi - midi_max + 11) // 12)
            n.pitch.midi += octaves * 12
            adjusted += 1
        elif midi < midi_min:
            octaves = (midi_min - midi + 11) // 12
            n.pitch.midi += octaves * 12
            adjusted += 1

    return adjusted


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

    # Remove title and credit text boxes (they cause large top spacing in MuseScore)
    transposed.metadata = metadata.Metadata()
    for tb in list(transposed.recurse().getElementsByClass(text.TextBox)):
        tb.activeSite.remove(tb)

    # Strip page layout entirely (causes top spacing issues)
    for el in list(transposed.recurse().getElementsByClass(layout.PageLayout)):
        el.activeSite.remove(el)

    # For system layout: keep system breaks (isNew=True) but clear dimension values
    # so MuseScore respects original line breaks without inheriting Audiveris spacing
    for el in list(transposed.recurse().getElementsByClass(layout.SystemLayout)):
        if el.isNew:
            el.topDistanceOdd = None
            el.topDistanceEven = None
            el.leftMargin = None
            el.rightMargin = None
            el.distance = None
        else:
            el.activeSite.remove(el)

    # Remove dynamics added by music21 that were not in the original OMR output
    for d in list(transposed.recurse().getElementsByClass(dynamics.Dynamic)):
        d.activeSite.remove(d)

    adjusted = fit_to_range(transposed, target)
    if adjusted:
        print(f"Range adjustment: {adjusted} note(s) shifted by octave to fit {target['name']} range")

    transposed.write("musicxml", fp=output_path)
    print(f"Output written to {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print(__doc__)
        sys.exit(1)

    _, input_path, source_key, target_key, output_path = sys.argv
    transpose_score(input_path, source_key, target_key, output_path)
