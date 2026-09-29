
import uiautomator2 as u2
import subprocess
import os
import csv
import random
import time
import re
import cv2
import traceback
DEVICE_ID="ROQKZT8PKJQODM5D"

if not(os.path.exists(r"C:\Users\ROG STRIX G15\Desktop\tiktok_project\dataSetScrapper\data\data.csv")) :
            with open(r"C:\Users\ROG STRIX G15\Desktop\tiktok_project\dataSetScrapper\data\data.csv","a",newline="") as f :
                writer = csv.writer(f)
                writer.writerow(["id","captions","hashtags","text_on_screen","label"])
        
d = u2.connect(DEVICE_ID)



def extract_caption_hashtags():
        caption_element=d(resourceId="com.zhiliaoapp.musically:id/desc")
        photo_element=d(resourceId="com.zhiliaoapp.musically:id/ycf")
        if not(caption_element.exists) or photo_element.exists:
             return [None,None]
        else:     
            try:
                caption_hashtags_text=caption_element.get_text()
                if re.search(r"more\b",caption_element.get_text()) :
                    more_button = d(resourceId="com.zhiliaoapp.musically:id/byp").info["bounds"]
                    c_more=center(more_button["left"],more_button["top"],more_button["right"],more_button["bottom"])
                    d.click(c_more[0],c_more[1])
                    caption_element.wait_gone(timeout=1.0)
                    caption_element=d(resourceId="com.zhiliaoapp.musically:id/desc")
                    caption_hashtags_text = caption_element.get_text()
                    time.sleep(1)
                    less_button=d(resourceId="com.zhiliaoapp.musically:id/z71").info["bounds"]
                    c_less=center(less_button["left"],less_button["top"],less_button["right"],less_button["bottom"])
                    d.click(c_less[0],c_less[1])
            except Exception as e:
                print("--- Error Detail ---")
                traceback.print_exc()
            if caption_element.exists : 
                parts=caption_hashtags_text.split('#',1)
                if len(parts) == 2:
                    return [parts[0],"#"+parts[1]]
                else :
                    if "#" not in parts[0]:
                        return [parts[0],None]
                    else :
                         return [None,parts[0]]
            
def center(left,top,right,bottom):
    cx= int((left+right)/2)
    cy= int((top+bottom)/2)
    return [cx,cy]



def extract_screenshot(index):
        device_pic_path=r"C:\Users\ROG STRIX G15\Desktop\tiktok_project\dataSetScrapper\data\screenshots"
        border_elem = d(resourceId="com.zhiliaoapp.musically:id/bol")
        if border_elem.exists:
            borders=border_elem.info["bounds"]
            left = borders["left"]
            right = int(borders["right"] - borders["right"] * 0.15)
            top = int(borders["top"] + (borders["bottom"] - borders["top"]) * 0.20)
            bottom = borders["bottom"]            
        if not os.path.exists(device_pic_path):
            os.path.mkdir(device_pic_path)

        img=d.screenshot(format="opencv")
        cropped_img=img[top:bottom,left:right] #[vertical range,horizental range]
        try:
            cv2.imwrite(os.path.join(device_pic_path,f"{index}.png"),cropped_img) # cv2.imwrite(path,img)
            print("screenshot has been saved succesfuly")
        except Exception as e : 
            print("Error occured :",e)
    
def swipe_next_video():

    width, height = d.window_size()
    start_x = width // 2 + random.randint(1,10)
    start_y = int(height * 0.8) + random.randint(1,10)
    end_x = width // 2 + random.randint(1,5)
    end_y = int(height * 0.3) + random.randint(1,10)
    rand_steps = random.randint(5,10)

    if random.randint(1,3) == 1 :
        d.swipe_ext("up", scale=0.8)
    else:
        d.swipe(start_x, start_y, end_x, end_y, steps=rand_steps)

"""
def send_like():
    like_button = d(resourceId="com.zhiliaoapp.musically:id/faq")
    if like_button.wait(timeout=2.0) : 
        like_boundaries= like_button.info["bounds"]
        like_c = center(like_boundaries["left"],like_boundaries["top"],like_boundaries["right"],like_boundaries["bottom"])
        d.click(like_c[0],like_c[1])
"""

def send_like(label):

    doLike = random.random()
    if label == 0:
        if doLike <= 0.05 :
            like_button = d(resourceId="com.zhiliaoapp.musically:id/faq")
            if like_button.wait(timeout=2.0) : 
                like_boundaries= like_button.info["bounds"]
                like_c = center(like_boundaries["left"],like_boundaries["top"],like_boundaries["right"],like_boundaries["bottom"])
                d.click(like_c[0],like_c[1])
    elif label==1:
        if doLike > 0.05:
            like_button = d(resourceId="com.zhiliaoapp.musically:id/faq")
            if like_button.wait(timeout=2.0) : 
                like_boundaries= like_button.info["bounds"]
                like_c = center(like_boundaries["left"],like_boundaries["top"],like_boundaries["right"],like_boundaries["bottom"])
                d.click(like_c[0],like_c[1])





        
