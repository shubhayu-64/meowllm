"""MeowLM configuration."""

from dataclasses import dataclass


@dataclass
class MeowConfig:
    vocab_size: int = 4096
    max_seq_len: int = 128
    d_model: int = 256
    n_layers: int = 4
    n_heads: int = 4
    ffn_hidden: int = 512
    dropout: float = 0.1

    pad_id: int = 0
    bos_id: int = 1
    eos_id: int = 2


@dataclass
class TrainConfig:
    batch_size: int = 32
    learning_rate: float = 3e-4
    min_lr: float = 3e-5
    weight_decay: float = 0.1
    warmup_steps: int = 200
    max_steps: int = 10000
    eval_interval: int = 200
    save_interval: int = 500
    grad_clip: float = 1.0
    device: str = "auto"
    seed: int = 42
    data_dir: str = "data"
    output_dir: str = "checkpoints"
