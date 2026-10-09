"""Runs inside the container. Loads Kokoro once, then turns each stdin line into a wav.

Protocol (stdout): READY once the model is loaded, then DONE or ERROR <msg> per line.
"""
import argparse
import sys

import numpy as np
import soundfile as sf
from kokoro import KPipeline

parser = argparse.ArgumentParser()
parser.add_argument("--lang", default="a", help="'a' = American English, 'j' = Japanese")
parser.add_argument("--voice", default="af_heart", help="e.g. af_heart, jf_alpha")
parser.add_argument("--out", default="speak.wav")
args = parser.parse_args()

pipeline = KPipeline(lang_code=args.lang)
print("READY", flush=True)

for line in sys.stdin:
    text = line.strip()
    try:
        chunks = [np.asarray(audio) for _, _, audio in pipeline(text, voice=args.voice)]
        sf.write(args.out, np.concatenate(chunks), 24000)
        print("DONE", flush=True)
    except Exception as e:  # keep the loop alive on bad input
        print(f"ERROR {e}", flush=True)
