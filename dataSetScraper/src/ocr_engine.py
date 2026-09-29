import cv2
import easyocr
import os
import re


SCREENSHOTS_PATH = r"C:\Users\ROG STRIX G15\Desktop\tiktok_project\dataSetScrapper\data\screenshots"
reader = easyocr.Reader(['en','fr'],gpu=True)

def readImg(index):
    img = cv2.imread(os.path.join(SCREENSHOTS_PATH,f"{index}.png"))
    return img




def extract_text(nparr):
    result = reader.readtext(nparr,paragraph=False,x_ths=0.8)

    cleaned_txt_list = []
    if not result : 
        return ""
    for item in result:
        if len(item) == 3 : 
            bounds,txt,conf=item
            if conf >= 0.9:
                if not( re.search(r"\b(Explore|Following|For You|@)\b",txt) or "@" in txt)  : 
                    cleaned_txt_list.append(txt)
        else :
            bounds,txt=item
            if not( re.search(r"\b(Explore|Following|For You)\b",txt) or "@" in txt ) : 
                cleaned_txt_list.append(txt)
    

   
    txt=" ".join(cleaned_txt_list)

    return txt





