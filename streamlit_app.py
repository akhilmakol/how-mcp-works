from __future__ import annotations

import json
import os
from pathlib import Path
import sys

MPL_CACHE_DIR = Path(__file__).resolve().parent / ".streamlit" / "matplotlib"
MPL_CACHE_DIR.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(MPL_CACHE_DIR))

import matplotlib.pyplot as plt
import streamlit as st
import torch

SRC_PATH = Path(__file__).resolve().parent / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from how_mcp_works.data import build_tokenizer_and_data
from how_mcp_works.inference import load_checkpoint


st.set_page_config(page_title="How MCP Works", layout="wide")

st.title("How MCP Works")
st.caption("A visual, interactive walkthrough of what MCP is, why we need it, and how it is implemented step by step.")

corpus_path = Path("data") / "corpus.txt"
checkpoint_path = Path("artifacts") / "checkpoint.pt"
scenarios_path = Path("data") / "scenarios.json"

with st.sidebar:
    st.header("Controls")
    prompt = st.text_area("Ask about MCP", value="what is mcp: ")
    max_new_tokens = st.slider("New tokens", min_value=10, max_value=200, value=80, step=10)
    temperature = st.slider("Temperature", min_value=0.2, max_value=1.8, value=0.9, step=0.1)
    top_k = st.slider("Top-k", min_value=1, max_value=20, value=8, step=1)

if not checkpoint_path.exists():
    st.warning("No trained checkpoint found yet. Run `python -m scripts.train` first.")
    st.stop()

model, tokenizer, checkpoint = load_checkpoint(checkpoint_path)
model.eval()

intro_col, concept_col = st.columns([1.3, 1])
with intro_col:
    st.subheader("Prompt to Tokens")
    encoded = tokenizer.encode(prompt) if prompt else [0]
    st.write("Encoded token IDs:")
    st.code(str(encoded))

with concept_col:
    st.subheader("What this project explains")
    st.markdown(
        """
        - what MCP is
        - why MCP is useful
        - how hosts, clients, and servers interact
        - how tools, resources, and prompts fit into an implementation
        """
    )

input_ids = torch.tensor([encoded], dtype=torch.long)
context_ids = input_ids[:, -model.config.block_size :]

with torch.no_grad():
    logits, _ = model(context_ids)
    next_logits = logits[0, -1]
    probs = torch.softmax(next_logits / temperature, dim=-1)
    top_probs, top_indices = torch.topk(probs, k=min(top_k, probs.shape[0]))
    generated = model.generate(
        context_ids,
        max_new_tokens=max_new_tokens,
        temperature=temperature,
        top_k=top_k,
    )[0].tolist()

st.subheader("Top Next-Token Candidates")
fig, ax = plt.subplots(figsize=(8, 4))
labels = [repr(tokenizer.itos[idx.item()]) for idx in top_indices]
ax.bar(labels, top_probs.tolist(), color="#2a6f97")
ax.set_ylabel("Probability")
ax.set_xlabel("Candidate token")
ax.set_title("Model belief while continuing an MCP explanation")
st.pyplot(fig)

result_col, details_col = st.columns(2)
with result_col:
    st.subheader("Generated Explanation")
    st.code(tokenizer.decode(generated), language="text")

with details_col:
    st.subheader("Checkpoint Summary")
    st.json(
        {
            "model_config": checkpoint["model_config"],
            "training_config": checkpoint["training_config"],
            "metrics": checkpoint["metrics"],
        }
    )

st.subheader("Interactive MCP Scenarios")
if scenarios_path.exists():
    scenarios = json.loads(scenarios_path.read_text(encoding="utf-8"))
    selected_title = st.selectbox("Choose a scenario", [item["title"] for item in scenarios])
    selected = next(item for item in scenarios if item["title"] == selected_title)
    scenario_col, insight_col = st.columns(2)
    with scenario_col:
        st.markdown(f"**Concept:** {selected['concept']}")
        st.write(selected["scenario"])
    with insight_col:
        st.markdown("**What to notice**")
        st.write(selected["what_to_notice"])

st.subheader("Corpus Snapshot")
_, data = build_tokenizer_and_data(corpus_path)
st.write(f"Corpus length: {len(data)} tokens")
st.text(corpus_path.read_text(encoding="utf-8")[:600])
