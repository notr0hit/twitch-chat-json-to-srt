from inspect import stack
import json
from datetime import timedelta
import os
import tkinter as tk
from tkinter import filedialog
from collections import deque

from cv2 import FileNode_NAMED

def get_json_data(json_file_path):
    with open(json_file_path, 'r', encoding="utf8") as json_file:
        json_load = json.load(json_file)

    return json_load


def get_tokens(json_file, no_of_chats):
    info = []
    # We will maintain a queue
    deq = deque()
    for comment in json_file['comments']:
        cur_info = {}
        cur_info["user_name"] = comment['commenter']['display_name']
        cur_info['user_color'] = comment['message']['user_color']
        cur_info['comment'] = comment['message']['body']
        cur_info['start_time'] = str(timedelta(seconds=comment['content_offset_seconds']))
        cur_info['end_time'] = str(timedelta(seconds=10000000000))
        cur_info['offset'] = comment['content_offset_seconds']
        deq.append(cur_info)
        
        if len(deq) >= no_of_chats:
            last_info = deq.popleft()
            last_info['end_time'] = str(timedelta(seconds=(cur_info['offset']-0.1)))     
            info.append(last_info)
    
    while (len(deq)):
        last_info = deq.popleft()
        last_info['end_time'] = str(timedelta(seconds=(last_info['offset']+10)))      
        info.append(last_info)
    
    return info


def build_srt(infos, srt_file_name, font_size):
    fp = open(srt_file_name, 'a', encoding='utf8')
    ind = 1
    for info in infos:
        fp.write(
        "{}\n{} -->  {}\n<font color={} size={}>{}</font> <font size={}>: {}</font>\n\n".format(
            ind, info['start_time'], info['end_time'], 
            info['user_color'], font_size, info['user_name'],
            font_size, info['comment'] )
            )
        ind += 1

    fp.close()
    return 

def select_srt_file():
    root = tk.Tk()
    root.withdraw()
    json_file = filedialog.askopenfilename()
    return json_file

print("Select json file.")
json_file = select_srt_file()
if not json_file.endswith('json'):
    print("Please select json file first! ")
    exit(0)

no_of_chats = 1
str_no_of_chats = (input("Enter maximum number of chats simultaneously (default=1) : "))
if str_no_of_chats.isdigit():
    no_of_chats = int(str_no_of_chats)

font_size = 12
str_font_size = (input("Enter font size (default = 10) : "))
if str_font_size.isdigit():
    font_size = int(str_font_size)

srt_file_name = str(os.path.basename(json_file))[:-5] + '.srt'
os.chdir(os.path.dirname(json_file))
fp = open(srt_file_name, 'w', encoding="utf8")
fp.close()

json = get_json_data(json_file)
infos = get_tokens(json, no_of_chats)
build_srt(infos, srt_file_name, font_size)

print("Success, srt file saved as {}.".format(srt_file_name))
