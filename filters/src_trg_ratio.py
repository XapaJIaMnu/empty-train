#!/usr/bin/env python3
"""Filters the lines based on the ratio between num_src_tokens and num_trg_tokens"""
from sys import stdin, stdout, stderr
from typing import Optional
import argparse


def parse_user_args():
    """Parse the arguments necessary for this filter"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--ratio-length", default=0.6, type=float)
    parser.add_argument("--debug", action='store_true')
    return parser.parse_args()

def clean_parallel(ratio: float, debug: Optional[bool]=True) -> None:
    """Cleans the parallel dataset based on the ratio of source to target tokens and vice versa"""
    for line in stdin:
        fields = line.strip().split('\t')
        if len(fields) != 2:
            stderr.write(f'SINGLE/MULTIPLE_LINES\t{line.strip()}')
            continue

        src = fields[-2].strip()
        trg = fields[-1].strip()

        # Remove identical lines
        if src.lower() == trg.lower():
            stderr.write(f'IDENTICAL\t{src}\t{trg}')
            continue

        src_toks = src.split()
        trg_toks = trg.split()
        src_len = len(src_toks)
        trg_len = len(trg_toks)

        ratio_len = src_len / float(trg_len)
        if ratio_len < ratio or ratio_len > (1. / ratio):
            if debug:
                stderr.write(f'RATIO_LENGTH\t{src}\t{trg}')
        else:
            stdout.write(line)

if __name__ == '__main__':
    args = parse_user_args()
    clean_parallel(args.ratio_length, args.args.debug)
