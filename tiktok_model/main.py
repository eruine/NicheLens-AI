"""
tiktok_model/main.py
====================
Entry point for training a niche classifier.

Usage:
    python main.py --niche "brawl stars game" --data ../dataSetScrapper/data/data.csv
    python main.py --niche "minecraft" --data ./data/data.csv --model-name minecraft

The trained model is saved to:
    models/<model-name>.pkl       (default model-name = niche with spaces → underscores)
"""

import argparse
import os
import sys

# Allow `from src.xxx import` when running from tiktok_model/
sys.path.insert(0, os.path.dirname(__file__))

from src.train_nich import train


def parse_args():
    parser = argparse.ArgumentParser(
        description="Train a TikTok niche classifier from a labeled dataset."
    )
    parser.add_argument(
        "--niche",
        type=str,
        required=True,
        help='Name of the niche this model is for. Used to name the output file. '
             'Example: --niche "brawl stars game"',
    )
    parser.add_argument(
        "--data",
        type=str,
        required=True,
        help="Path to the labeled CSV dataset. "
             "Example: --data ../dataSetScrapper/data/data.csv",
    )
    parser.add_argument(
        "--model-name",
        type=str,
        default=None,
        help="Custom filename (without .pkl) for the saved model. "
             "Defaults to the niche name with spaces replaced by underscores.",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    data_path = os.path.abspath(args.data)
    if not os.path.exists(data_path):
        raise SystemExit(f"Error: dataset not found: {data_path}")

    model_name = args.model_name or args.niche.lower().replace(" ", "_")
    models_dir = os.path.join(os.path.dirname(__file__), "models")
    os.makedirs(models_dir, exist_ok=True)
    model_path = os.path.join(models_dir, f"{model_name}.pkl")

    print(f"[main] niche      = '{args.niche}'")
    print(f"[main] dataset    = {data_path}")
    print(f"[main] model out  = {model_path}\n")

    train(dataset_path=data_path, model_path=model_path)

    print(f"\n[main] Done. To use this model in the bot:\n")
    print(f"  cd ../dataSetScrapper")
    print(f"  python bot.py --model {model_path}\n")


if __name__ == "__main__":
    main()
