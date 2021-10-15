import os
import sys
import json


ARGV = list()

def get_settings(settings_file_path):
    settings_result = None
    try:
        with open(os.path.abspath(settings_file_path), "r") as settings_file:
            settings_result = json.loads(settings_file.read())
    except FileNotFoundError:
        print("settings.json file not found.")

    argv = sys.argv[1:]
    settings_argv = list()
    flag = False
    for i in sys.argv[1:]:
        if i.startswith("-"):
            flag = True
        if flag:
            settings_argv.append(i)
        else:
            ARGV.append(i) 
    
    i_max = len(settings_argv)
    i = 0
    while i < i_max:
        setting = settings_argv[i]
        if setting.startswith("-"):
            value = settings_argv[i+1]
            i+=1
            settings_result[setting[1:]] = json.loads(value)
        i+=1
    
    return settings_result

#get the settings from settings.json file
SETTINGS = get_settings("settings.json")

if __name__=="__main__":
    print(ARGV)
    print(SETTINGS)
