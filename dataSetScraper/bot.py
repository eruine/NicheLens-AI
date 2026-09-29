import argparse
import src.ocr_engine as ocr_engine
import src.scraper as scraper
import src.storage as storage
import random
import json
import traceback
import time


def parse_args():
    parser = argparse.ArgumentParser(
        description="TikTok engagement bot — likes posts that match the given niche."
    )
    parser.add_argument(
        "--niche",
        type=str,
        help=(
            'Niche keyword used by the AI labelizer. '
            'Required unless --model is provided. '
            'Example: --niche "brawl stars game"'
        ),
    )
    parser.add_argument(
        "--model",
        type=str,
        default=None,
        help="Path to a trained .pkl model file. If provided, uses ML model instead of AI labelizer.",
    )
    parser.add_argument(
        "--target",
        type=int,
        default=500,
        help="Number of matched posts before stopping (default: 500)",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    target = args.target

    # Choose classification backend: trained model OR AI labelizer
    if args.model:
        import joblib
        from src import storage as _storage

        pipeline = joblib.load(args.model)
        print(f"[bot] Using trained model: {args.model}\n")

        def classify(caption, hashtags, text_on_screen):
            cap = _storage.clean_text(caption or "")
            hsh = _storage.clean_text(hashtags or "")
            txt = _storage.clean_text(text_on_screen or "")
            full = f"{cap} {hsh} {txt}"
            pred = pipeline.predict([full])[0]
            return {"label": int(pred)}

    else:
        if not args.niche:
            raise SystemExit("Error: --niche is required when --model is not provided.")

        import src.labelaizer as labelaizer

        niche = args.niche
        print(f"[bot] Using AI labelizer  niche='{niche}'\n")

        def classify(caption, hashtags, text_on_screen):
            while True:
                try:
                    raw = labelaizer.labelize(caption, hashtags, text_on_screen, niche)
                    return json.loads(raw)
                except Exception:
                    print(f"json error! : {traceback.print_exc()}")

    counter_0 = 0
    counter_1 = 0
    index = 0

    while counter_0 < target or counter_1 < target:

        caption_hashtags = scraper.extract_caption_hashtags()
        print("cap : ", caption_hashtags)

        if caption_hashtags[0] is not None or caption_hashtags[1] is not None:

            img = ocr_engine.readImg(index)
            txt = ocr_engine.extract_text(img)
            print("text on screen : ", txt, "\n")

            label = classify(caption_hashtags[0], caption_hashtags[1], txt)
            print(f"{label}\n")

            lv = int(label["label"])

            if lv == 1 and counter_1 < target:
                scraper.send_like(lv)
                counter_1 += 1
                index += 1
            elif lv == 0 and counter_0 < target:
                scraper.send_like(lv)
                counter_0 += 1
                index += 1

        print(f"index_0 : {counter_0}\nindex_1 : {counter_1}\n")

        lv = label.get("label", 0)
        randomtime = random.randint(5, 12)
        if lv == 0:
            if random.random() <= 0.05:
                time.sleep(randomtime)
        else:
            if random.random() > 0.05:
                time.sleep(randomtime)

        scraper.swipe_next_video()


if __name__ == "__main__":
    main()
