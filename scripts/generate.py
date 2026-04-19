from __future__ import annotations

import argparse
from pathlib import Path

import torch

from ._bootstrap import ensure_src_on_path

ensure_src_on_path()

from how_mcp_works.inference import load_checkpoint_and_generate


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate beginner-friendly text about banking fundamentals.")
    parser.add_argument("--checkpoint-path", type=Path, default=Path("artifacts") / "checkpoint.pt")
    parser.add_argument("--prompt", type=str, default="banking concept: savings account")
    parser.add_argument("--max-new-tokens", type=int, default=120)
    parser.add_argument("--temperature", type=float, default=0.9)
    parser.add_argument("--top-k", type=int, default=8)
    parser.add_argument("--device", type=str, default="cuda" if torch.cuda.is_available() else "cpu")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    text = load_checkpoint_and_generate(
        checkpoint_path=args.checkpoint_path,
        prompt=args.prompt,
        max_new_tokens=args.max_new_tokens,
        temperature=args.temperature,
        top_k=args.top_k,
        device=args.device,
    )
    print(text)


if __name__ == "__main__":
    main()
