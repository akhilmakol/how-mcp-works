# Contributing

Contributions of code, documentation, examples, tests, and issue reports are welcome.

## Before You Contribute

1. Review the existing issues and pull requests.
2. Open an issue for substantial changes so direction can be discussed early.
3. Keep changes scoped to a clear problem statement.

## Pull Requests

Please aim to:

- keep pull requests focused and reviewable
- include tests when behavior changes
- update documentation when user-facing behavior changes
- explain the motivation and expected outcome clearly

## Commit Sign-Off

Where practical, sign commits using the Developer Certificate of Origin style sign-off:

```text
Signed-off-by: Your Name <your.email@example.com>
```

Using `git commit -s` is the easiest way to do this.

## Development Workflow

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .[dev]
python -m scripts.train --steps 20 --eval-interval 10
python -m scripts.generate --prompt "banking concept: interest"
```

## Community Expectations

By participating in this project, you agree to follow [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

