import json
import os.path

json_file = open('C:\\Code\\Jarvis\\prompts\\tools.json')
toolData = json.load(json_file)

def getToolData():
    return toolData

prompts = {}
prompt_paths = ["C:\\Code\\Jarvis\\prompts\\toolRetrievalPrompt.txt", "C:\\Code\\Jarvis\\prompts\\planning_prompt.txt"]

for i in prompt_paths:
    prompt_file_content = ""
    file = open(i, "r")
    prompt_file_content += file.read()
    prompts[os.path.basename(i)] = prompt_file_content
    file.close()


def getPrompt(file_name):
    return prompts[file_name]