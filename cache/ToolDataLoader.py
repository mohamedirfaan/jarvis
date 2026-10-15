import json
import os.path

json_file = open('/home/irfaan-24083/jarvis/prompts/tools.json')
toolData = json.load(json_file)

def getToolData():
    return toolData

prompts = {}
prompt_paths = ["/home/irfaan-24083/jarvis/prompts/toolRetrievalPrompt.txt", "/home/irfaan-24083/jarvis/prompts/planning_prompt.txt"]

for i in prompt_paths:
    prompt_file_content = ""
    file = open(i, "r")
    prompt_file_content += file.read()
    prompts[os.path.basename(i)] = prompt_file_content
    file.close()


def getPrompt(file_name):
    return prompts[file_name]