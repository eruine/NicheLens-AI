import csv
import re

to_string = lambda x: x or ""

black_listed_words = set([
            "a", "an", "the", "and", "or", "but", "if", "while",
            "is", "am", "are", "was", "were","till",
            "be", "been", "being","end",
            "to", "of", "in", "on", "at",
            "for", "with", "as", "by",
            "this", "that", "these", "those",
            "it", "its",
            "he", "she", "they", "them",
            "my", "your", "his", "her",
            "we", "us","like",
            "likes","comment","comments","share",
            "save","live","sound","shop","reply",
            "replies"
])

black_listed_sentences = set([
    "like and share",
    "comment below",
    "tag someone",
    "tag your friend",
    "double tap",
    "don't forget to",
    "link in bio",
    "check bio",
    "Full screen",
    "subscribe",
    "follow me",
    "new post",
    "#fyp","#foryou","##foryou","#viral","#trending",
    "#tiktok","#explore","following","#fyp","#foryou","#foryoupage",
    "#viral","#trending","#trend","#xyzbca","#tiktok","#tiktokviral",
    "#reels","#shorts","#video","#explorepage","#instagood","#like4like",
    "#follow4follow",
    "watch till the end",
    "wait for it"
])

def store_all(index,cap_hash,text_on_screen,label):
    
    if cap_hash[0] != None or cap_hash[1] != None :
        with open(r"C:\Users\ROG STRIX G15\Desktop\tiktok_project\dataSetScrapper\data\data.csv","a",encoding="utf-8-sig",newline="") as f:
             writer = csv.writer(f)
             cap_to_str = to_string(cap_hash[0])
             cap_to_str = to_string(cap_to_str if len(cap_to_str.split()) <= 20 else " ".join(cap_to_str.split()[:20]))
             hash_to_str = to_string(cap_hash[1])
             writer.writerow([index,clean_text(cap_to_str),clean_text(hash_to_str),clean_text(text_on_screen),label])
        return True
    return False

def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z#\-_\s]", " ", text)
    text = text.replace("’","'")
    #\b is what we call a "Word Boundary."
    for txt in black_listed_sentences :
        text = re.sub(re.escape(txt.lower()),"",text) #It turns it into "Contact\ us\?", telling Python: "Treat this literally as text, not as a special code."
    cleaned_txt = [txt for txt in text.split() if txt.lower() not in black_listed_words ]
    text = " ".join(cleaned_txt)
    text = re.sub(r"\s+", " ", text)
    return text.strip()
