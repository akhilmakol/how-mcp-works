from how_mcp_works.tokenizer import CharTokenizer


def test_tokenizer_round_trip() -> None:
    tokenizer = CharTokenizer.from_text("abc cab")
    text = "cab"
    assert tokenizer.decode(tokenizer.encode(text)) == text

