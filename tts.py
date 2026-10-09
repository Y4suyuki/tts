import argparse

import numpy as np
import soundfile as sf
from kokoro import KPipeline

parser = argparse.ArgumentParser(description="Kokoro TTS")
parser.add_argument("text")
parser.add_argument("--lang", default="a", help="'a' = American English, 'j' = Japanese")
parser.add_argument("--voice", default="af_heart", help="e.g. af_heart, jf_alpha")
parser.add_argument("--out", default="/out/out.wav")
args = parser.parse_args()

pipeline = KPipeline(lang_code=args.lang)
chunks = [np.asarray(audio) for _, _, audio in pipeline(args.text, voice=args.voice)]
sf.write(args.out, np.concatenate(chunks), 24000)
print(f"wrote {args.out}")
