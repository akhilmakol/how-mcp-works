import torch

from how_mcp_works.config import ModelConfig
from how_mcp_works.model import MiniGPT


def test_model_forward_shape() -> None:
    config = ModelConfig(vocab_size=16, block_size=8, n_layers=2, n_heads=2, n_embed=16)
    model = MiniGPT(config)
    idx = torch.randint(0, config.vocab_size, (4, config.block_size))
    logits, loss = model(idx, idx)
    assert logits.shape == (4, config.block_size, config.vocab_size)
    assert loss is not None


def test_model_generate_extends_sequence() -> None:
    config = ModelConfig(vocab_size=12, block_size=8, n_layers=1, n_heads=2, n_embed=16)
    model = MiniGPT(config)
    idx = torch.randint(0, config.vocab_size, (1, 4))
    generated = model.generate(idx, max_new_tokens=5)
    assert generated.shape[1] == 9

