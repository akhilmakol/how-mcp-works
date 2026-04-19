from __future__ import annotations

from pathlib import Path

import torch

from .tokenizer import CharTokenizer


def load_corpus(path: str | Path) -> str:
    return Path(path).read_text(encoding="utf-8")


def build_tokenizer_and_data(path: str | Path) -> tuple[CharTokenizer, torch.Tensor]:
    text = load_corpus(path)
    tokenizer = CharTokenizer.from_text(text)
    data = torch.tensor(tokenizer.encode(text), dtype=torch.long)
    return tokenizer, data


def split_data(data: torch.Tensor, train_split: float) -> tuple[torch.Tensor, torch.Tensor]:
    split_idx = int(len(data) * train_split)
    return data[:split_idx], data[split_idx:]


def get_batch(
    source: torch.Tensor,
    batch_size: int,
    block_size: int,
    device: str,
) -> tuple[torch.Tensor, torch.Tensor]:
    max_start = len(source) - block_size - 1
    if max_start < 1:
        raise ValueError("Dataset is too small for the selected block size.")

    starts = torch.randint(0, max_start, (batch_size,))
    x = torch.stack([source[i : i + block_size] for i in starts])
    y = torch.stack([source[i + 1 : i + block_size + 1] for i in starts])
    return x.to(device), y.to(device)

