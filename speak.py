#!/usr/bin/env python3
"""Runs on the Mac. Type a line, hear it spoken. Ctrl-D or Ctrl-C to quit.

Usage:  python3 speak.py                          # English
        python3 speak.py --lang j --voice jf_alpha  # Japanese
"""
import readline  # noqa: F401  (line editing + history for input())
import subprocess
import sys

# How to start the server inside the container. Extra CLI args are passed through.
SERVER_CMD = [
    "devcontainer", "exec", "--workspace-folder", ".",
    "python", "speak_server.py",
] + sys.argv[1:]
WAV = "speak.wav"  # written by the server into the shared project folder

log = open("speak.log", "w")
server = subprocess.Popen(
    SERVER_CMD, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=log, text=True, bufsize=1
)


def wait_for(*markers: str) -> str:
    """Skip unrelated output until the server prints one of the markers."""
    for line in server.stdout:
        if line.split(" ", 1)[0].strip() in markers:
            return line.strip()
    sys.exit("server exited — see speak.log")


print("loading model...")
wait_for("READY")

try:
    while True:
        text = input("> ").strip()
        if not text:
            continue
        server.stdin.write(text + "\n")
        server.stdin.flush()
        reply = wait_for("DONE", "ERROR")
        if reply.startswith("ERROR"):
            print(reply)
        else:
            subprocess.run(["afplay", WAV])
except (EOFError, KeyboardInterrupt):
    print()
finally:
    server.terminate()
