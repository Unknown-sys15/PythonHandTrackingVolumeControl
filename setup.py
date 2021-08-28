import json


target_fps = input("target fps: ")
smoothness = input('smoothness :')
url = input("URL = https://--ip address of your phone--:8080/video --> ")

config = {}
config['info'] = []
config['info'].append({
    'target_fps': str(target_fps),
    'smoothness': smoothness,
    'url': url
})

with open('config.json', 'w') as f:
    json.dump(config, f, ensure_ascii=False, indent=4)
