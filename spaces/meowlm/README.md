---
title: MeowLM
emoji: 🐱
colorFrom: orange
colorTo: yellow
sdk: gradio
sdk_version: "4.44.0"
app_file: app.py
pinned: false
license: mit
short_description: Chat with a tiny cat language model in your browser
---

# MeowLM

Interactive demo for [MeowLM](https://github.com/arman-bd/guppylm) — a ~4M parameter decoder-only transformer trained on synthetic cat conversations.

## Setup (repo owner)

1. Train MeowLM and export weights (see repo `tools/export_meow_model.py`).
2. Push to a **model** repo, e.g. `your-username/meowlm-4M`, containing:
   - `pytorch_model.bin`
   - `config.json`
   - `tokenizer.json`
3. Create a **Space** on Hugging Face → **Gradio** → link this folder (or push `spaces/meowlm` as the Space repo).
4. In Space **Settings → Repository variables**, set:
   - `MODEL_REPO` = `your-username/meowlm-4M`
5. Space **Hardware**: CPU Basic is enough; GPU makes cold start faster.

Public URL: `https://huggingface.co/spaces/<user>/meowlm`
