from __future__ import annotations

import json
import random
from dataclasses import asdict
from pathlib import Path

import torch

from .config import ModelConfig, TrainingConfig
from .data import get_batch, split_data
from .model import MiniGPT
from .tokenizer import CharTokenizer


def set_seed(seed: int) -> None:
    random.seed(seed)
    torch.manual_seed(seed)


@torch.no_grad()
def estimate_loss(
    model: MiniGPT,
    train_data: torch.Tensor,
    val_data: torch.Tensor,
    train_config: TrainingConfig,
) -> dict[str, float]:
    model.eval()
    metrics: dict[str, float] = {}
    for split_name, source in {"train": train_data, "val": val_data}.items():
        losses = torch.zeros(train_config.eval_batches)
        for i in range(train_config.eval_batches):
            x, y = get_batch(source, train_config.batch_size, model.config.block_size, train_config.device)
            _, loss = model(x, y)
            losses[i] = loss.item()
        metrics[split_name] = losses.mean().item()
    model.train()
    return metrics


def save_checkpoint(
    path: str | Path,
    model: MiniGPT,
    tokenizer: CharTokenizer,
    model_config: ModelConfig,
    training_config: TrainingConfig,
    metrics: dict[str, float],
) -> None:
    payload = {
        "model_state_dict": model.state_dict(),
        "tokenizer": tokenizer.to_dict(),
        "model_config": asdict(model_config),
        "training_config": asdict(training_config),
        "metrics": metrics,
    }
    torch.save(payload, path)


def write_metrics(path: str | Path, metrics: dict[str, float]) -> None:
    Path(path).write_text(json.dumps(metrics, indent=2), encoding="utf-8")


def train(
    data: torch.Tensor,
    tokenizer: CharTokenizer,
    model_config: ModelConfig,
    training_config: TrainingConfig,
    output_dir: str | Path,
) -> dict[str, float]:
    set_seed(training_config.seed)
    train_data, val_data = split_data(data, training_config.train_split)
    model = MiniGPT(model_config).to(training_config.device)
    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=training_config.learning_rate,
        weight_decay=training_config.weight_decay,
    )

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    last_metrics = {"train": float("nan"), "val": float("nan")}
    for step in range(training_config.steps):
        if step % training_config.eval_interval == 0 or step == training_config.steps - 1:
            last_metrics = estimate_loss(model, train_data, val_data, training_config)
            print(
                f"step {step:04d} | train loss {last_metrics['train']:.4f} | "
                f"val loss {last_metrics['val']:.4f}"
            )

        xb, yb = get_batch(train_data, training_config.batch_size, model_config.block_size, training_config.device)
        _, loss = model(xb, yb)
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        optimizer.step()

    checkpoint_path = output_dir / "checkpoint.pt"
    save_checkpoint(checkpoint_path, model, tokenizer, model_config, training_config, last_metrics)
    write_metrics(output_dir / "metrics.json", last_metrics)
    return last_metrics

