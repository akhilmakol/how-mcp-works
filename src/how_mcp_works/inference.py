from __future__ import annotations

from pathlib import Path

import torch

from .config import ModelConfig
from .model import MiniGPT
from .tokenizer import CharTokenizer


def load_checkpoint(path: str | Path, device: str = "cpu") -> tuple[MiniGPT, CharTokenizer, dict]:
    checkpoint = torch.load(path, map_location=device)
    model_config = ModelConfig(**checkpoint["model_config"])
    tokenizer = CharTokenizer.from_dict(checkpoint["tokenizer"])
    model = MiniGPT(model_config)
    model.load_state_dict(checkpoint["model_state_dict"])
    model.to(device)
    model.eval()
    return model, tokenizer, checkpoint


@torch.no_grad()
def generate_text(
    model: MiniGPT,
    tokenizer: CharTokenizer,
    prompt: str,
    max_new_tokens: int,
    temperature: float = 1.0,
    top_k: int | None = None,
    device: str = "cpu",
) -> str:
    encoded = tokenizer.encode(prompt) if prompt else [0]
    input_ids = torch.tensor([encoded], dtype=torch.long, device=device)
    output_ids = model.generate(
        input_ids,
        max_new_tokens=max_new_tokens,
        temperature=temperature,
        top_k=top_k,
    )[0].tolist()
    return tokenizer.decode(output_ids)


def load_checkpoint_and_generate(
    checkpoint_path: str | Path,
    prompt: str,
    max_new_tokens: int = 120,
    temperature: float = 1.0,
    top_k: int | None = None,
    device: str = "cpu",
) -> str:
    model, tokenizer, _ = load_checkpoint(checkpoint_path, device=device)
    return generate_text(
        model=model,
        tokenizer=tokenizer,
        prompt=prompt,
        max_new_tokens=max_new_tokens,
        temperature=temperature,
        top_k=top_k,
        device=device,
    )
