"""MeowLM inference for the Hugging Face Space."""

import json
import os

import torch
from tokenizers import Tokenizer

from config import MeowConfig
from model import MeowLM


class MeowInference:
    def __init__(self, checkpoint_path, tokenizer_path, device="cpu"):
        self.device = torch.device(device)
        self.tokenizer = Tokenizer.from_file(tokenizer_path)

        ckpt = torch.load(checkpoint_path, map_location=self.device, weights_only=False)
        config_dir = os.path.dirname(os.path.abspath(checkpoint_path))
        config_path = os.path.join(config_dir, "config.json")

        if isinstance(ckpt, dict) and "model_state_dict" in ckpt:
            state_dict = ckpt["model_state_dict"]
        else:
            state_dict = ckpt

        if os.path.exists(config_path):
            with open(config_path) as f:
                cfg = json.load(f)
            self.config = MeowConfig(
                vocab_size=cfg.get("vocab_size", 4096),
                max_seq_len=cfg.get("max_position_embeddings", cfg.get("max_seq_len", 128)),
                d_model=cfg.get("hidden_size", cfg.get("d_model", 256)),
                n_layers=cfg.get("num_hidden_layers", cfg.get("n_layers", 4)),
                n_heads=cfg.get("num_attention_heads", cfg.get("n_heads", 4)),
                ffn_hidden=cfg.get("intermediate_size", cfg.get("ffn_hidden", 512)),
                dropout=cfg.get("hidden_dropout_prob", cfg.get("dropout", 0.1)),
                pad_id=cfg.get("pad_token_id", cfg.get("pad_id", 0)),
                bos_id=cfg.get("bos_token_id", cfg.get("bos_id", 1)),
                eos_id=cfg.get("eos_token_id", cfg.get("eos_id", 2)),
            )
        elif isinstance(ckpt, dict) and "config" in ckpt:
            valid_fields = {f.name for f in MeowConfig.__dataclass_fields__.values()}
            self.config = MeowConfig(**{k: v for k, v in ckpt["config"].items() if k in valid_fields})
        else:
            self.config = MeowConfig()

        self.model = MeowLM(self.config).to(self.device)
        filtered = {k: v for k, v in state_dict.items() if k in self.model.state_dict()}
        self.model.load_state_dict(filtered)
        self.model.eval()

    def chat_completion(self, messages, temperature=0.7, max_tokens=64, top_k=50, **kwargs):
        prompt = self._format_prompt(messages)
        input_ids = self.tokenizer.encode(prompt).ids
        prompt_tokens = len(input_ids)
        input_t = torch.tensor([input_ids], dtype=torch.long, device=self.device)
        output_t, _ = self.model.generate(input_t, max_tokens, temperature, top_k)
        output_text = self.tokenizer.decode(output_t[0].tolist()[prompt_tokens:])
        if "<|im_end|>" in output_text:
            output_text = output_text.split("<|im_end|>")[0]
        if "<|im_start|>" in output_text:
            output_text = output_text.split("<|im_start|>")[0]
        return {
            "choices": [{"message": {"role": "assistant", "content": output_text.strip()}}],
        }

    def _format_prompt(self, messages):
        parts = []
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content") or ""
            if role == "system":
                continue
            parts.append(f"<|im_start|>{role}\n{content}<|im_end|>")
        parts.append("<|im_start|>assistant\n")
        return "\n".join(parts)
