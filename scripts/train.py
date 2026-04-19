from __future__ import annotations

import argparse
from pathlib import Path

import torch

from ._bootstrap import ensure_src_on_path

ensure_src_on_path()

from how_mcp_works.config import ModelConfig, TrainingConfig
from how_mcp_works.data import build_tokenizer_and_data
from how_mcp_works.trainer import train


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train a tiny GPT-style character model.")
    parser.add_argument("--corpus-path", type=Path, default=Path("data") / "corpus.txt")
    parser.add_argument("--output-dir", type=Path, default=Path("artifacts"))
    parser.add_argument("--steps", type=int, default=300)
    parser.add_argument("--eval-interval", type=int, default=50)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--block-size", type=int, default=64)
    parser.add_argument("--n-layers", type=int, default=3)
    parser.add_argument("--n-heads", type=int, default=4)
    parser.add_argument("--n-embed", type=int, default=128)
    parser.add_argument("--dropout", type=float, default=0.1)
    parser.add_argument("--learning-rate", type=float, default=3e-4)
    parser.add_argument("--device", type=str, default="cuda" if torch.cuda.is_available() else "cpu")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    tokenizer, data = build_tokenizer_and_data(args.corpus_path)
    model_config = ModelConfig(
        vocab_size=tokenizer.vocab_size,
        block_size=args.block_size,
        n_layers=args.n_layers,
        n_heads=args.n_heads,
        n_embed=args.n_embed,
        dropout=args.dropout,
    )
    training_config = TrainingConfig(
        steps=args.steps,
        eval_interval=args.eval_interval,
        batch_size=args.batch_size,
        learning_rate=args.learning_rate,
        device=args.device,
    )
    metrics = train(data, tokenizer, model_config, training_config, args.output_dir)
    print(f"Training complete. Final metrics: {metrics}")


if __name__ == "__main__":
    main()
