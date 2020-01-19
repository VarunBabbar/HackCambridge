import json
import os.path

def json_write(data):
    with open('data.txt', 'w') as outfile:
        json.dump(data, outfile)

def json_read():
    print("hello world")