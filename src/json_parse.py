import json
import os.path

def json_write(data):
    with open('data.txt', 'w') as outfile:
        json.dump(data, outfile,ensure_ascii=False, indent=4)

def json_read():
    print("hello world")