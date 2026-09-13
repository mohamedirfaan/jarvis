import json

json_file = open('C:\\Code\\Jarvis\\prompts\\tools.json')
toolData = json.load(json_file)

def getToolData():
    return toolData