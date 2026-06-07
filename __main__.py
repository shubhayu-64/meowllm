"""Entry point: python -m meowlm"""

import os
import sys

CHECKPOINT_PATH = "checkpoints/best_model.pt"
TOKENIZER_PATH = "data/tokenizer.json"
CONFIG_PATH = "checkpoints/config.json"
HF_REPO = os.environ.get("HF_MEOW_REPO", "arman-bd/meowlm-4M")
HF_BASE = f"https://huggingface.co/{HF_REPO}/resolve/main"


def download_model():
    import urllib.request

    files = [
        (f"{HF_BASE}/pytorch_model.bin", CHECKPOINT_PATH),
        (f"{HF_BASE}/tokenizer.json", TOKENIZER_PATH),
        (f"{HF_BASE}/config.json", CONFIG_PATH),
    ]

    print(f"Downloading MeowLM from {HF_REPO}...\n")
    for url, dest in files:
        os.makedirs(os.path.dirname(dest) or ".", exist_ok=True)
        name = os.path.basename(dest)
        print(f"  {name}...", end=" ", flush=True)
        urllib.request.urlretrieve(url, dest)
        print(f"{os.path.getsize(dest) / 1e6:.1f} MB")

    print("\nDone! Run: python -m meowlm chat")


def main():
    if len(sys.argv) < 2:
        print("MeowLM — a tiny cat brain")
        print()
        print("Usage:")
        print("  python -m meowlm prepare      Generate data & train tokenizer")
        print("  python -m meowlm train        Train the model")
        print("  python -m meowlm chat         Chat with Meow")
        print("  python -m meowlm download     Download pre-trained weights from HuggingFace")
        return

    cmd = sys.argv[1]
    sys.argv = sys.argv[1:]

    if cmd == "prepare":
        from .prepare_data import prepare
        prepare()
    elif cmd == "train":
        from .train import train
        train()
    elif cmd == "download":
        download_model()
    elif cmd == "chat":
        if not os.path.exists(CHECKPOINT_PATH):
            print("Model not found. Download first:\n\n  python -m meowlm download\n")
            return
        from .inference import main as inference_main
        inference_main()
    else:
        print(f"Unknown command: {cmd}")


main()
