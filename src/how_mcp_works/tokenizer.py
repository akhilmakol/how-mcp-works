from __future__ import annotations

from dataclasses import dataclass


UNK_TOKEN = "<unk>"


@dataclass(slots=True)
class CharTokenizer:
    stoi: dict[str, int]
    itos: dict[int, str]

    @classmethod
    def from_text(cls, text: str) -> "CharTokenizer":
        vocab = [UNK_TOKEN] + sorted(set(text))
        stoi = {ch: i for i, ch in enumerate(vocab)}
        itos = {i: ch for ch, i in stoi.items()}
        return cls(stoi=stoi, itos=itos)

    @property
    def vocab_size(self) -> int:
        return len(self.stoi)

    def encode(self, text: str) -> list[int]:
        unk_id = self.stoi[UNK_TOKEN]
        return [self.stoi.get(ch, unk_id) for ch in text]

    def decode(self, token_ids: list[int]) -> str:
        return "".join("?" if self.itos[idx] == UNK_TOKEN else self.itos[idx] for idx in token_ids)

    def to_dict(self) -> dict[str, dict]:
        return {"stoi": self.stoi, "itos": {str(k): v for k, v in self.itos.items()}}

    @classmethod
    def from_dict(cls, payload: dict[str, dict]) -> "CharTokenizer":
        stoi = {str(k): int(v) for k, v in payload["stoi"].items()}
        itos = {int(k): v for k, v in payload["itos"].items()}
        return cls(stoi=stoi, itos=itos)
