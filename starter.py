# coding: utf-8

import requests
import json
from pprint import pprint
from datetime import datetime
import re
from datetime import datetime
from config import config 
from optparse import OptionParser

#Methods that connect with external sources
def getDoingIssues():
    openedIssuesJson = getIssues(False)
    listDoingIssues = []
    for issue in openedIssuesJson:
        if("Doing" in issue["labels"]):
            listDoingIssues.append(issue)

    return listDoingIssues

def postOnSlack(string):
    payload={"channel": config.SLACK_CHANNEL, "username": "Blamer", "text": string, "icon_emoji": ":japanese_ogre:"}
    r = requests.post(config.SLACK_URL, json=payload)

def updateIssue(issueId, data):
    headers = {"PRIVATE-TOKEN": "Uz6PgmkmEiZ3yHvWX8D9"}
    r = requests.put(config.GITLAB_URL+"/issues/"+str(issueId)+"?"+data, headers=headers)
    #r.encoding = "ISO-8859-1"
    newJson = json.loads(r.text)

    return newJson

def getIssues(closed):
    #Queries Gitlab API for closed/open issues of our project
    if(closed):
        typeQuery = "closed"
    else:
        typeQuery = "opened"

    finalJson = json.loads("[]")
    endLoop = False
    #It Requires pagination to get all issues
    page = 1
    numberItems = 50
    while not endLoop:
        headers = {"PRIVATE-TOKEN": "Uz6PgmkmEiZ3yHvWX8D9"}
        r = requests.get(config.GITLAB_URL+"/issues?page="+str(page)+"&per_page="+str(numberItems)+"&state="+typeQuery+"&order_by=updated_at&sort=asc", headers=headers)
        r.encoding = "utf-8"
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
    r = requests.get(config.GITLAB_URL+"issues/"+str(issueId), headers=config.HEADERS_GITLAB)
    r.encoding = "ISO-8859-1"
    return json.loads(r.text)
    
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
    jsonIssues = getIssues(True) 
    for issue in jsonIssues:
        addDueDate(issue)

def blameDueDates():
    #Finds closed issues than dont have a dueDate
    jsonIssues = getIssues(True) 
    textToBlame = ""
    for issue in jsonIssues:
        if(issue["due_date"] is None):
            if(issue["assignee"]["name"] in dictPeople):
                user = "<"+config.TEAM_MEMBERS[issue["assignee"]["name"]]+">"
            else:
                user = issue["assignee"]["name"]

            #textToBlame += user+": la tarea _"+issue["title"]+"_ no tiene due date, <"+issue["web_url"]+"| pincha aquí>\n"
            textToBlame += "{user}: la tarea _{title}_ no tiene due date, <{web_url}| pincha aquí> para solucionarlo\n".format(user=user,title=issue["title"], web_url=issue["web_url"])

    postOnSlack(textToBlame)

def blameDoingIssues():
    issues = getDoingIssues()
    textToBlame = ""
    for issue in issues:
        if(issue["assignee"] is not None):
            noPt = False
            for label in issue["labels"]:
                if("pt" in label):
                    noPt = True
            if(not noPt):
                textToBlame += "{user}: la tarea _{title}_ no tiene puntos estimados, <{web_url}| pincha aquí> para solucionarlo\n".format(user="<"+config.TEAM_MEMBERS[issue["assignee"]["name"]]+">",title=issue["title"], web_url=issue["web_url"])
        else:
            textToBlame += "Equipo, la tarea _{title}_ no está asignada a nadie, <{web_url}| pinchad aquí> para solucionarlo\n".format(title=issue["title"], web_url=issue["web_url"])
    postOnSlack(textToBlame)

def addDueDate(issue):
    #If there's no due date we set it as the closest Monday of the updated date
    if(issue["due_date"] is None):
        updated = datetime.strptime(issue["updated_at"], "%Y-%m-%dT%H:%M:%S.%fZ")
        print(issue["title"]+" : "+updated.strftime('%Y-%m-%d')+" - "+issue["updated_at"])    
        data = "due_date="+updated.strftime('%Y-%m-%d')
        updateIssue(issue["id"], data)

def printAllClosedIssues():
    jsonIssues = getIssues(True) 
    print(json.dumps(jsonIssues, indent=4, sort_keys=True))  

def printAllOpenIssues():
    jsonIssues = getIssues(False) 
    print(json.dumps(jsonIssues, indent=4, sort_keys=True))   

def countAllSprints():
    #Loops through all issues and calculates the points of each of the sprints
    dictSprints = {}
    jsonIssues = getIssues(True)   

    for issue in jsonIssues:
        #Check what sprint an issue belongs to
        dueDate = issue["due_date"]
        if(dueDate is not None):
            dictPoints = countPoints(issue)
            #Add the points of that sprint
            tempDict = {"estimated" : 0, "done" : 0} if dueDate not in dictSprints else dictSprints[dueDate]
            tempDict["estimated"] += dictPoints["estimated"]
            tempDict["done"] += dictPoints["done"]

            dictSprints[dueDate] = tempDict

    pprint(dictSprints)   

def printIssuesFromSprint(dateSprint):
    jsonIssues = getIssues(True) 
    listIssues = []
    for issue in jsonIssues:
        if(issue["due_date"] == dateSprint):
            pprint(issue)


def calculateClosingSprint():
    #We only run it on Mondays
    #if(datetime.now().weekday() != 0):
    #    print("Today is not Monday!")
    #    return
    jsonIssues = getIssues(True)   
    estimatedPoints = 0
    donePoints = 0
    dictTeamMembers = {}
    for issue in jsonIssues:
        if(issue["due_date"] is not None):
            dateClosed = datetime.strptime(issue["due_date"], "%Y-%m-%d")
            diff = datetime.now() - dateClosed
            # If the issue was belongs on this closing sprint we process it
            if(diff.days <= 7):
                pointsC = countPoints(issue)
                estimatedPoints += pointsC["estimated"]
                donePoints += pointsC["done"]
                tempDict = {} if issue["assignee"]["name"] not in dictTeamMembers else dictTeamMembers[issue["assignee"]["name"]]
                tempDict["estimated"] = pointsC["estimated"]
                tempDict["done"] = pointsC["done"]
                dictTeamMembers[issue["assignee"]["name"]] = tempDict

    stringMembers = ""

    for key, value in dictTeamMembers.items():
        stringMembers += config.TEAM_MEMBERS[key]+": *"+str(dictTeamMembers[key]["estimated"])+"pts estimados*,  *"+str(dictTeamMembers[key]["done"])+" pts hechos*\n"

    postOnSlack("Atención, estas son las métricas de esta semana:\n *Tareas hechas: "+str(donePoints)+" puntos*\n *Estimadas: "+str(estimatedPoints)+"puntos*\n"+stringMembers)

def dailyIssuesCheck():
    blameDoingIssues()
    blameDueDates()

def main():
    parser = OptionParser(usage="usage: %prog [options] filename",
                          version="%prog 1.0")
    parser.add_option("-m","--method",dest="method",help="The name of the method to be executed, calculateClosingSprint, countAllSprints, dailyIssuesCheck")

    (options, args) = parser.parse_args() 

    print("Executing "+options.method)

    result = {
      'calculateClosingSprint' : calculateClosingSprint,
      'countAllSprints': countAllSprints,
      'dailyIssuesCheck': dailyIssuesCheck
    }

    result[options.method]()
    
if __name__ == '__main__':
    main()