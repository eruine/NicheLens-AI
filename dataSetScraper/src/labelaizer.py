from ollama import Client
import src.storage as storage

client = Client()

to_string = lambda x: x or ""


def labelize(caption, hashtags, text_on_screen, niche):
    """
    Ask the LLM whether a TikTok post belongs to the given niche.

    Args:
        caption (str | None):         Post caption text.
        hashtags (str | None):        Post hashtags string.
        text_on_screen (str | None):  Text extracted from the video frame via OCR.
        niche (str):                  The target niche, e.g. "brawl stars game".

    Returns:
        str: Raw JSON string with format {"label": 0|1|2}
             1 = belongs to niche, 0 = does not, 2 = unsure.
    """
    caption        = storage.clean_text(to_string(caption))
    hashtags       = storage.clean_text(to_string(hashtags))
    text_on_screen = storage.clean_text(to_string(text_on_screen))

    messages = [
        {
            "role": "user",
            "content": (
                f"You are a binary classifier for TikTok posts.\n"
                f"Given:\n"
                f"  Caption: {caption}\n"
                f"  Hashtags: {hashtags}\n"
                f"  Text on screen: {text_on_screen}\n\n"
                f"Does this post belong to the \"{niche}\" niche?\n"
                f"Return ONLY valid JSON with the format: {{\"label\": value}}\n"
                f"  value = 1 → yes\n"
                f"  value = 0 → no\n"
                f"  value = 2 → unsure\n"
                f"No explanation. No extra text. Just the JSON."
            ),
        }
    ]

    response = ""
    try:
        for part in client.chat("gpt-oss:120b-cloud", messages=messages, stream=True):
            response += part["message"]["content"]
    except Exception:
        return None

    return response
