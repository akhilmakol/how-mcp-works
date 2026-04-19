from pathlib import Path

from ._bootstrap import ensure_src_on_path

ensure_src_on_path()

from how_mcp_works.data import build_tokenizer_and_data


def main() -> None:
    corpus_path = Path("data") / "corpus.txt"
    tokenizer, data = build_tokenizer_and_data(corpus_path)
    print(f"Loaded corpus from {corpus_path}")
    print(f"Vocabulary size: {tokenizer.vocab_size}")
    print(f"Total tokens: {len(data)}")


if __name__ == "__main__":
    main()
