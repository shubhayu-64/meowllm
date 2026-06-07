"""
Orchestration script for MeowLM.

This script executes the entire MeowLM pipeline sequentially:
1. Dataset Generation & Tokenizer Training
2. Model Training
3. Model Evaluation
"""

import argparse
import logging
import os
import sys

from prepare_data import prepare
from train import train
from inference import MeowInference
from eval_cases import get_eval_cases

# Configure basic logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)


def run_data_preparation(data_dir: str, n_samples: int, eval_ratio: float):
    """Generate synthetic data and train the BPE tokenizer."""
    logger.info("=== STEP 1: Data Preparation ===")
    try:
        prepare(data_dir=data_dir, n_samples=n_samples, eval_ratio=eval_ratio)
        logger.info("Data preparation completed successfully.")
    except Exception as e:
        logger.error(f"Failed during data preparation: {e}")
        sys.exit(1)


def run_training():
    """Execute the PyTorch training loop."""
    logger.info("=== STEP 2: Model Training ===")
    try:
        train()
        logger.info("Model training completed successfully.")
    except Exception as e:
        logger.error(f"Failed during model training: {e}")
        sys.exit(1)


def run_evaluation(checkpoint_path: str, tokenizer_path: str, device: str = "cpu"):
    """Evaluate the trained model against hand-authored test cases."""
    logger.info("=== STEP 3: Model Evaluation ===")

    if not os.path.exists(checkpoint_path):
        logger.warning(f"Checkpoint not found at {checkpoint_path}. Attempting fallback.")
        fallback_path = os.path.join(os.path.dirname(checkpoint_path), "final_model.pt")
        if os.path.exists(fallback_path):
            checkpoint_path = fallback_path
            logger.info(f"Using fallback checkpoint: {checkpoint_path}")
        else:
            logger.error(f"No trained model found. Please ensure training completed successfully.")
            sys.exit(1)

    if not os.path.exists(tokenizer_path):
        logger.error(f"Tokenizer not found at {tokenizer_path}.")
        sys.exit(1)

    logger.info("Initializing inference engine...")
    try:
        engine = MeowInference(checkpoint_path, tokenizer_path, device=device)
    except Exception as e:
        logger.error(f"Failed to initialize inference engine: {e}")
        sys.exit(1)

    cases = get_eval_cases()
    passed = 0

    print("\n" + "-" * 60)
    print("EVALUATION RESULTS")
    print("-" * 60)

    for case in cases:
        prompt = case["prompt"]
        expect_keywords = case["expect_keywords"]
        
        msgs = [{"role": "user", "content": prompt}]
        
        try:
            result = engine.chat_completion(msgs, temperature=0.7, max_tokens=64)
            response = result["choices"][0]["message"]["content"].lower()
        except Exception as e:
            logger.error(f"Error generating response for prompt '{prompt}': {e}")
            continue
        
        # Check if at least one expected keyword is present
        found_keywords = [kw for kw in expect_keywords if kw.lower() in response]
        success = len(found_keywords) > 0
        
        if success:
            passed += 1
            status = "✅ PASS"
        else:
            status = "❌ FAIL"
            
        print(f"{status} | Prompt: '{prompt}'")
        print(f"       | MeowLM: '{response}'")
        if not success:
            print(f"       | Expected at least one of: {expect_keywords}")
        print("-" * 60)

    logger.info(f"Evaluation Complete! Passed {passed}/{len(cases)} cases.")


def main():
    parser = argparse.ArgumentParser(description="MeowLM End-to-End Pipeline")
    parser.add_argument("--data-dir", type=str, default="data", help="Directory for data and tokenizer")
    parser.add_argument("--samples", type=int, default=120000, help="Number of samples to generate")
    parser.add_argument("--eval-ratio", type=float, default=0.05, help="Ratio of eval data to total data")
    parser.add_argument("--checkpoint", type=str, default="checkpoints/best_model.pt", help="Path to best model checkpoint")
    parser.add_argument("--device", type=str, default="cpu", help="Device for evaluation (cpu, cuda, mps)")
    parser.add_argument("--skip-data", action="store_true", help="Skip data generation and tokenizer training")
    parser.add_argument("--skip-train", action="store_true", help="Skip model training")
    parser.add_argument("--skip-eval", action="store_true", help="Skip model evaluation")
    
    args = parser.parse_args()

    if not args.skip_data:
        run_data_preparation(args.data_dir, args.samples, args.eval_ratio)
    
    if not args.skip_train:
        run_training()
        
    if not args.skip_eval:
        tokenizer_path = os.path.join(args.data_dir, "tokenizer.json")
        run_evaluation(args.checkpoint, tokenizer_path, args.device)
        
    logger.info("Pipeline execution finished.")


if __name__ == "__main__":
    main()
