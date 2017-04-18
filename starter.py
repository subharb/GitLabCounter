# coding: utf-8

import requests
import json
from pprint import pprint
from datetime import datetime
import re
from datetime import datetime

#Methods that connect with external sources
def postOnSlack(string):
    payload={"channel": "#gitlab-notifications", "username": "Blamer", "text": string, "icon_emoji": ":japanese_ogre:"}
    r = requests.post("https://hooks.slack.com/services/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", json=payload)

def updateIssue(issueId, data):
    headers = {"PRIVATE-TOKEN": "Uz6PgmkmEiZ3yHvWX8D9"}
    r = requests.put("http://git.augmentedworkforce.com/api/v3/projects/17/issues/"+str(issueId)+"?"+data, headers=headers)
    #r.encoding = "ISO-8859-1"
    newJson = json.loads(r.text)

    return newJson

def getClosedIssues():
    #Queries Gitlab API for closed issues of our project
    finalJson = json.loads("[]")
    endLoop = False
    #It Requires pagination to get all issues
    page = 1
    numberItems = 50
    while not endLoop:
        headers = {"PRIVATE-TOKEN": "Uz6PgmkmEiZ3yHvWX8D9"}
        r = requests.get("http://git.augmentedworkforce.com/api/v3/projects/17/issues?page="+str(page)+"&per_page="+str(numberItems)+"&state=closed&order_by=updated_at&sort=asc", headers=headers)
        r.encoding = "ISO-8859-1"
        newJson = json.loads(r.text)
        if(len(finalJson) > 0):
            for element in newJson:
                finalJson.append(element)    
            
        else:
            finalJson = newJson
        page += 1
        if(len(newJson) < numberItems):
            endLoop = True
    
    return finalJson

def getInfoIssue(issueId):
    headers = {"PRIVATE-TOKEN": "Uz6PgmkmEiZ3yHvWX8D9"}
    r = requests.get("https://git.augmentedworkforce.com/api/v3/projects/17/issues/"+str(issueId), headers=headers)
    r.encoding = "ISO-8859-1"
    print(json.loads(r.text))
    
def getRawNumberPoints(string):
    #Deletes letters from label
    return int(re.findall("\d", string)[0])

def countPoints(issue):
    #Returns dictionary, on "estimated" key the estimated points, and "done", the done points
    points = {"estimated" : 0, "done" : 0}
    for label in issue["labels"]:      
        if("Est." in label):    
            #Deletes letters from label
            points["estimated"] = getRawNumberPoints(label)
        elif("pt" in label):
            points["done"] = getRawNumberPoints(label)
    #If there aren't any "Estimated" labels we add the done points, because it was correctly estimated
    if(points["estimated"] == 0):
        points["estimated"] = points["done"]
    return points

def fixAllDueDates():
    jsonIssues = getClosedIssues() 
    for issue in jsonIssues:
        addDueDate(issue)

def blameDueDates():
    dictPeople = {"smartipo" : "@smartipo", "Angela" : "@aruiztej", "Elena" : "@elenavj", "Merixell" : "@meritxell"}
    jsonIssues = getClosedIssues() 
    textToBlame = ""
    for issue in jsonIssues:
        if(issue["due_date"] is None):
            if(issue["assignee"]["name"] in dictPeople):
                user = "<"+dictPeople[issue["assignee"]["name"]]+">"
            else:
                user = issue["assignee"]["name"]

            textToBlame += user+": la tarea _"+issue["title"]+"_ no tiene due date, <"+issue["web_url"]+"| pincha aqui>\n"
            #textToBlame += "{user}: la tarea _{title}_ no tiene due date, <{web_url}}| pincha aquí>".format(user=user,title=issue["title"], web_url=issue["web_url"])

    postOnSlack(textToBlame)

def addDueDate(issue):
    #If there's no due date we set it as the closest Monday of the updated date
    if(issue["due_date"] is None):
        updated = datetime.strptime(issue["updated_at"], "%Y-%m-%dT%H:%M:%S.%fZ")
        print(issue["title"]+" : "+updated.strftime('%Y-%m-%d')+" - "+issue["updated_at"])    
        data = "due_date="+updated.strftime('%Y-%m-%d')
        updateIssue(issue["id"], data)

def printAllClosedIssues():
    jsonIssues = getClosedIssues() 
    print(json.dumps(jsonIssues, indent=4, sort_keys=True))   
        
def start():
    #We only run it on Mondays
    if(datetime.now().weekday() != 0):
        return
    jsonIssues = getClosedIssues()   
    estimatedPoints = 0
    donePoints = 0 
    for issue in jsonIssues:
        #If the issue was closed last week I process it
        dateClosed = datetime.strptime(issue["due_date"], "%Y-%m-%d")
        diff = datetime.now() - dateClosed
        if(diff.days < 7):
            pointsC = countPoints(issue)
            estimatedPoints += pointsC["estimated"]
            donePoints += pointsC["done"]        

    print("Done: "+str(donePoints))
    print("Estimate: "+str(estimatedPoints))
if __name__ == '__main__':
    #start()
    blameDueDates()
    #addDueDate()