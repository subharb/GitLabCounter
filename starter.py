# coding: utf-8

import requests
import json
from pprint import pprint
from datetime import datetime
import re
from datetime import datetime

def updateIssue(issueId, data):
    
    headers = {"PRIVATE-TOKEN": "Uz6PgmkmEiZ3yHvWX8D9"}
    r = requests.put("http://git.augmentedworkforce.com/api/v3/projects/17/issues/"+str(issueId)+"?"+data, headers=headers)
    #r.encoding = "ISO-8859-1"
    newJson = json.loads(r.text)

    print(newJson)

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
        
        
        '''if(page==3):
            print(json.dumps(finalJson, indent=4, sort_keys=True))
            return
'''
    
    return finalJson

def getInfoIssue():
    headers = {"PRIVATE-TOKEN": "Uz6PgmkmEiZ3yHvWX8D9"}
    r = requests.get("https://git.augmentedworkforce.com/api/v3/projects/17/issues/76", headers=headers)
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

def addDueDate():
    jsonIssues = getClosedIssues() 
    for issue in jsonIssues:
        #If there's no due date we set it as the closest Monday of the updated date
        if(issue["due_date"] is None):
            print(issue["title"]+" : "+str(issue["id"])+" - "+issue["updated_at"])    

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
    addDueDate()