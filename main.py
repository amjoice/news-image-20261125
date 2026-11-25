#!/usr/bin/env python3
"""Entry program for make.fun news-image-20261125.

Copies the pre-rendered entry.png shipped in this repository to the
output directory. Standard library only, no network, deterministic:
every run writes the same bytes.
"""
import os
import shutil


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(source, os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
