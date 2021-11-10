import os
import sys
import json

def get_settings_and_argv(settings_file_path):
    settings_result = None
    try:
        with open(settings_file_path, "r") as settings_file:
            settings_result = json.loads(settings_file.read())
    except FileNotFoundError:
        print("settings.json file not found.")
    
    result_argv = list()
    argv = sys.argv[1:]
    settings_argv = list()
    flag = False
    for i in sys.argv[1:]:
        if i.startswith("-"):
            flag = True
        if flag:
            settings_argv.append(i)
        else:
            result_argv.append(i) 
    
    i_max = len(settings_argv)
    try:
        i = 0
        while i < i_max:
            setting = settings_argv[i]
            if setting.startswith("-"):
                value = settings_argv[i+1]
                i+=1
                try:
                    value = json.loads(value)
                except json.decoder.JSONDecodeError:
                    value = json.loads(f'"{value}"')
                settings_result[setting[1:]] = value
            i+=1
    except IndexError:
        pass
    return settings_result, result_argv

if __name__=="__main__":
    SETTINGS = get_settings('settings.json')
    print(ARGV)
    print(SETTINGS)
