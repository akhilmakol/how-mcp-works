from dataclasses import dataclass


@dataclass(slots=True)
class ModelConfig:
    vocab_size: int
    block_size: int = 64
    n_layers: int = 3
    n_heads: int = 4
    n_embed: int = 128
    dropout: float = 0.1


@dataclass(slots=True)
class TrainingConfig:
    batch_size: int = 32
    learning_rate: float = 3e-4
    weight_decay: float = 1e-2
    steps: int = 300
    eval_interval: int = 50
    eval_batches: int = 20
    seed: int = 42
    train_split: float = 0.9
    device: str = "cpu"

