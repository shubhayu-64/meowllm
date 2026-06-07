# Deploy MeowLM on Hugging Face (browser chat)

You need **two** Hugging Face repos:

1. **Model** — stores weights (`pytorch_model.bin`, `config.json`, `tokenizer.json`)
2. **Space** — runs the Gradio app visitors use in the browser

## Step 1 — Train and export the model

From the repo root (after `python -m meowlm prepare` and `python -m meowlm train`):

```bash
export HF_TOKEN=hf_...
python tools/export_meow_model.py \
  --checkpoint checkpoints/best_model.pt \
  --tokenizer data/tokenizer.json \
  --repo your-username/meowlm-4M
```

## Step 2 — Create the Space

1. Go to [huggingface.co/new-space](https://huggingface.co/new-space)
2. **Space name:** `meowlm` (or any name)
3. **SDK:** Gradio
4. **Hardware:** CPU basic (free tier is enough)
5. **Create from:** upload this folder, **or** link GitHub and set **Space directory** to `spaces/meowlm`

Upload these files (or push via git):

- `app.py`
- `config.py`, `model.py`, `inference.py`
- `requirements.txt`
- `README.md` (Space card with YAML header)

## Step 3 — Point the Space at your model

Space → **Settings** → **Repository variables** → add:

| Name | Value |
|------|--------|
| `MODEL_REPO` | `your-username/meowlm-4M` |

Rebuild the Space. Your public URL:

`https://huggingface.co/spaces/your-username/meowlm`

## Step 4 — Link from the model card

Edit the model repo README and set the Space badge URL to your Space.

## Optional — embed on the model page

On the model repo README, add:

```markdown
[![Open in HF Spaces](https://huggingface.co/datasets/huggingface/badges/resolve/main/open-in-hf-spaces-sm.svg)](https://huggingface.co/spaces/your-username/meowlm)
```

Hugging Face can also show a **Widget** on the model page if `pipeline_tag: text-generation` is set in the model card (already in `tools/meow_model_card.md`). The Gradio Space is still the best full chat UI.

## Alternative (like GuppyLM GitHub Pages)

Guppy uses **ONNX + WebAssembly** so inference runs **in the visitor’s browser** with no server. MeowLM does not have that export yet; the Gradio Space runs inference on Hugging Face’s servers instead. To add a client-only demo later, extend `tools/export_onnx.py` for MeowLM and host a static Space (`sdk: static`).
