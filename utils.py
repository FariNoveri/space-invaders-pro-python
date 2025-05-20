# utils.py
import os

def load_high_score(filename="high_score.txt"):
    if not os.path.exists(filename):
        return 0
    with open(filename, "r") as f:
        return int(f.read().strip())

def save_high_score(score, filename="high_score.txt"):
    with open(filename, "w") as f:
        f.write(str(score))
