"""
predictor.py
============
Loads a trained .pkl model and exposes a predict() function.
Used by bot.py as a drop-in replacement for the AI labelizer.
"""

import re
import joblib


def _clean_text(txt: str) -> str:
    txt = txt.lower()
    txt = re.sub(r"(.)\1{2,}", r"\1\1", txt)
    txt = re.sub(r"[^\s\d#a-zA-Z]", "", txt)
    txt = re.sub(r"\s{2,}", " ", txt)
    return txt.strip()


class NichePredictor:
    """
    Wraps a trained sklearn pipeline to classify TikTok posts.

    Usage:
        predictor = NichePredictor("models/brawlstars.pkl")
        label = predictor.predict(caption, hashtags, text_on_screen)
        # label → 0 (not niche) or 1 (niche)
    """

    def __init__(self, model_path: str):
        self.model_path = model_path
        self.pipeline   = joblib.load(model_path)
        print(f"[predictor] Model loaded: {model_path}")

    def predict(self, caption: str, hashtags: str, text_on_screen: str) -> int:
        cap = _clean_text(caption or "")
        hsh = _clean_text(hashtags or "")
        txt = _clean_text(text_on_screen or "")
        full_text = f"{cap} {hsh} {txt}"
        return int(self.pipeline.predict([full_text])[0])

    def predict_proba(self, caption: str, hashtags: str, text_on_screen: str) -> list[float]:
        """Returns [prob_class_0, prob_class_1]."""
        cap = _clean_text(caption or "")
        hsh = _clean_text(hashtags or "")
        txt = _clean_text(text_on_screen or "")
        full_text = f"{cap} {hsh} {txt}"
        return self.pipeline.predict_proba([full_text])[0].tolist()
