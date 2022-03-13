import json
from datetime import timedelta
import os
import tkinter as tk
from tkinter import filedialog
from turtle import end_fill

from cv2 import FileNode_NAMED

no_of_chats = 5

def get_json_data(json_file_path):
    with open(json_file_path, 'r', encoding="utf8") as json_file:
        json_load = json.load(json_file)

    return json_load


def get_info(json_file):
    info = []
    ind = 0
    json_file_list = list(json_file['comments'])
    for comment in json_file['comments']:
        cur_info = {}
        cur_info["user_name"] = comment['commenter']['display_name']
        cur_info['user_color'] = comment['message']['user_color']
        cur_info['comment'] = comment['message']['body']
        cur_info['start_time'] = str(timedelta(seconds=comment['content_offset_seconds']))
        if ind + no_of_chats < len(json_file['comments']):
            cur_info['end_time'] = str(
                timedelta(seconds=json_file_list[ind + no_of_chats]['content_offset_seconds'])
            )
        else:
            cur_info['end_time'] = str(
                timedelta(seconds=(json_file_list[ind]['content_offset_seconds'] + 3))
            )
        info.append(cur_info)
        ind += 1
    return info

def build_srt(infos, srt_file_name):
    fp = open(srt_file_name, 'a', encoding='utf8')
    ind = 1
    for info in infos:
        fp.write(
        "{}\n{} -->  {}\n<font color={}>{}</font>: {}\n\n".format(
            ind, info['start_time'], info['end_time'], 
            info['user_color'], info['user_name'], info['comment'] )
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

str_no_of_chats = (input("Enter maximum number of chats simultaneously (default=5) : "))
if str_no_of_chats != '' and str_no_of_chats.isdigit():
    no_of_chats = int(str_no_of_chats)

srt_file_name = str(os.path.basename(json_file))[:-5] + '.srt'
fp = open(srt_file_name, 'w', encoding="utf8")
fp.close()

json = get_json_data(json_file)
infos = get_info(json)
build_srt(infos, srt_file_name)

print("Success, srt file saved as {}.".format(srt_file_name))
