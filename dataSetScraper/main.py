import argparse
import src.labelaizer as labelaizer
import src.ocr_engine as ocr_engine
import src.scraper as scraper
import src.storage as storage
import random
import json
import traceback
import time


def parse_args():
    parser = argparse.ArgumentParser(
        description="TikTok dataset scraper — collects labeled posts for a given niche."
    )
    parser.add_argument(
        "--niche",
        type=str,
        required=True,
        help='The niche to classify posts for. Example: --niche "brawl stars game"',
    )
    parser.add_argument(
        "--target",
        type=int,
        default=500,
        help="Number of samples to collect per class (default: 500)",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    niche = args.niche
    target = args.target

    print(f"[scraper] niche='{niche}'  target={target} samples per class\n")

    counter_0 = 0
    counter_1 = 0
    index = 0

    while counter_0 < target or counter_1 < target:

        caption_hashtags = scraper.extract_caption_hashtags()
        print("cap : ", caption_hashtags)

        if caption_hashtags[0] is not None or caption_hashtags[1] is not None:

            scraper.extract_screenshot(index)
            img = ocr_engine.readImg(index)
            txt = ocr_engine.extract_text(img)
            print("text on screen : ", txt, "\n")

            while True:
                try:
                    label = labelaizer.labelize(
                        caption_hashtags[0], caption_hashtags[1], txt, niche
                    )
                    label = json.loads(label)
                    break
                except Exception:
                    print(f"json error! : {traceback.print_exc()}")

            print(f"{label}\n")

            if int(label["label"]) == 0 and counter_0 < target:
                storage.store_all(index, caption_hashtags, txt, label["label"])
                counter_0 += 1
                index += 1
            elif int(label["label"]) == 1 and counter_1 < target:
                storage.store_all(index, caption_hashtags, txt, label["label"])
                scraper.send_like(label["label"])
                counter_1 += 1
                index += 1

            print(f"index {index} --- data extraction : success\n")
        else:
            print("data extraction : failed\n")

        print(f"index_0 : {counter_0}\nindex_1 : {counter_1}\n")
        time.sleep(random.randint(5, 12))
        scraper.swipe_next_video()


if __name__ == "__main__":
    main()
