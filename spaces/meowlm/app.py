"""
MeowLM — Hugging Face Space demo.

Loads weights from a Hugging Face model repo (see MODEL_REPO) and serves a chat UI.
"""

import os

import gradio as gr
import torch
from huggingface_hub import snapshot_download

from inference import MeowInference

MODEL_REPO = os.environ.get("MODEL_REPO", "arman-bd/meowlm-4M")
_engine = None


def _pick_device() -> str:
    if torch.cuda.is_available():
        return "cuda"
    if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        return "mps"
    return "cpu"


def _pick_checkpoint(model_dir: str) -> str:
    for name in ("pytorch_model.bin", "best_model.pt", "model.pt"):
        path = os.path.join(model_dir, name)
        if os.path.exists(path):
            return path
    raise FileNotFoundError(
        f"No weights found in {model_dir}. Expected pytorch_model.bin or best_model.pt"
    )


def get_engine() -> MeowInference:
    global _engine
    if _engine is not None:
        return _engine

    print(f"Downloading MeowLM from {MODEL_REPO}...")
    model_dir = snapshot_download(repo_id=MODEL_REPO)
    checkpoint = _pick_checkpoint(model_dir)
    tokenizer = os.path.join(model_dir, "tokenizer.json")
    if not os.path.exists(tokenizer):
        raise FileNotFoundError(f"tokenizer.json not found in {model_dir}")

    device = _pick_device()
    print(f"Loading on {device}...")
    _engine = MeowInference(checkpoint, tokenizer, device=device)
    return _engine


def chat(message: str, history: list, temperature: float, max_tokens: int) -> str:
    if not message or not message.strip():
        return ""
    engine = get_engine()
    result = engine.chat_completion(
        [{"role": "user", "content": message.strip()}],
        temperature=temperature,
        max_tokens=int(max_tokens),
    )
    return result["choices"][0]["message"].get("content", "").strip() or "*stares at you*"


EXAMPLES = [
    ["psst psst psst", 0.7, 64],
    ["are you hungry?", 0.7, 64],
    ["look at the red dot", 0.8, 64],
    ["time for a bath", 0.7, 64],
    ["i filled your bowl", 0.7, 64],
    ["get off my keyboard", 0.7, 64],
    ["who's a good kitty?", 0.7, 64],
    ["the vacuum is on", 0.7, 64],
]

with gr.Blocks(title="MeowLM") as demo:
    gr.Markdown(
        """
# MeowLM
**A tiny language model that thinks it's in charge.**

Type like you're talking to a house cat. Replies are short, dramatic, and cat-brained.
Trained from scratch (~4M parameters). [Code on GitHub](https://github.com/arman-bd/guppylm).
        """
    )
    with gr.Row():
        temperature = gr.Slider(0.1, 1.5, value=0.7, step=0.05, label="Temperature")
        max_tokens = gr.Slider(16, 128, value=64, step=8, label="Max tokens")

    gr.ChatInterface(
        fn=chat,
        additional_inputs=[temperature, max_tokens],
        examples=EXAMPLES,
        title=None,
        description="Single-turn works best (128-token context). The cat may ignore you.",
    )

if __name__ == "__main__":
    demo.launch(theme=gr.themes.Soft())
