"""
train_nich.py
=============
Core training logic. Called by tiktok_model/main.py — do not run directly.
"""

import pandas as pd
import re
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report


def merge_fields(row) -> str:
    cap    = "" if pd.isna(row.get("captions"))       else str(row.get("captions"))
    hsh    = "" if pd.isna(row.get("hashtags"))       else str(row.get("hashtags"))
    txt_sc = "" if pd.isna(row.get("text_on_screen")) else str(row.get("text_on_screen"))
    return f"{cap} {hsh} {txt_sc}"


def clean_text(txt: str) -> str:
    txt = txt.lower()
    txt = re.sub(r"(.)\1{2,}", r"\1\1", txt)          # collapse repeated chars
    txt = re.sub(r"[^\s\d#a-zA-Z]", "", txt)           # keep alphanumeric + # + space
    txt = re.sub(r"\s{2,}", " ", txt)                  # normalize spaces
    return txt.strip()


def train(dataset_path: str, model_path: str) -> None:
    """
    Load dataset, train a TF-IDF + Logistic Regression pipeline, save to disk.

    Args:
        dataset_path: Path to the labeled CSV (columns: captions, hashtags, text_on_screen, label).
        model_path:   Where to save the trained .pkl pipeline.
    """
    print(f"[train] Loading dataset: {dataset_path}")
    df = pd.read_csv(dataset_path, encoding="utf-8-sig")
    df = df[df["label"].isin([0, 1])]

    df["full_text"] = df.apply(merge_fields, axis=1)
    df = df.drop_duplicates(subset=["full_text"])
    df["full_text"] = df["full_text"].apply(clean_text)

    x = df["full_text"]
    y = df["label"]

    X_train, X_test, Y_train, Y_test = train_test_split(
        x, y,
        test_size=0.2,
        random_state=42,
        stratify=y,   # keep class balance in both splits
    )

    word_vectorizer = TfidfVectorizer(
        analyzer="word",
        ngram_range=(1, 2),
        min_df=2,
        max_features=10_000,
    )
    char_vectorizer = TfidfVectorizer(
        analyzer="char",
        ngram_range=(3, 5),
        min_df=2,
        max_features=20_000,
    )

    pipeline = Pipeline([
        ("features", FeatureUnion([
            ("word", word_vectorizer),
            ("char", char_vectorizer),
        ])),
        ("classifier", LogisticRegression(max_iter=300, class_weight="balanced")),
    ])

    print("\n[train] Training ...\n")
    pipeline.fit(X_train, Y_train)

    print("[train] Evaluating ...\n")
    predictions = pipeline.predict(X_test)
    print(classification_report(Y_test, predictions))

    print(f"[train] Saving model → {model_path}\n")
    joblib.dump(pipeline, model_path)
    print("[train] Model saved successfully.\n")

    # Top contributing features
    feature_names = pipeline.named_steps["features"].get_feature_names_out()
    coefs         = pipeline.named_steps["classifier"].coef_[0]
    top_pos = sorted(zip(coefs, feature_names), reverse=True)[:20]
    top_neg = sorted(zip(coefs, feature_names))[:20]
    print("Top positive features:\n", top_pos)
    print("Top negative features:\n", top_neg)
