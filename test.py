import json


with open('config.json', 'r') as f:
    data = json.load(f)

list = data['info']
dict = {}
dict = list[0]
print(int(dict["target_fps"]))
print(int(dict["smoothness"]))
print(dict["url"])


def getJson(fileName):
    with open(fileName, 'r') as f:
        data = json.load(f)

    list = data['info']
    dict = {}
    dict = list[0]
    return int(dict["target_fps"]), int(dict["smoothness"]), dict["url"]


target_fps, smoothness, url = getJson('config.json')
print(target_fps)
print(smoothness)
print(url)


# AREA
# Pc 270 < area < 650
# Phone 950 < area < 3050
