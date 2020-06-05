import requests
import sys
import time
from bs4 import BeautifulSoup

globalresults = []
globalnumbers = []
globalemails = []



def robots(target): #we gonna do a respectful time
    response = requests.get(target + "/robots.txt") #post request to get html
    robotLines = response.text.split("\n") #sort html by line
    disallowed = [] # make empty list to store what's disallowed later
    for i in range(len(robotLines)):
        if robotLines[i].find("Disallow:") >= 0:  #Finding "Disallow:"
            disallowed.append(robotLines[i][10:]) #add to list, minus "Disallow: "
    return(disallowed)

def recur(target, tagTarget):
    if tagTarget.find("http") != -1:
        newTarget = tagTarget
    elif tagTarget.find("www") != -1:
        newTarget = tagTarget[tagTarget.find("www"):len(tagTarget)]
        newTarget = "https:" + tagTarget
    elif tagTarget.find("/") != 0:
        newTarget = target + "/" + tagTarget
    else:
        newTarget = target + tagTarget + ""
    response = requests.get(newTarget)
    soup = BeautifulSoup(response.text, "html.parser")
    allLinks = soup.find_all("a")
    if robotsCheck(robots(target), newTarget):
        for link in allLinks:
            text = str(link.get("href"))
            globalresults.append(text)
            time.sleep(5)


def robotsCheck(disallowed, target2):
    for x in disallowed:
        if x == target2:
            return False
    return True


def URLs(target):
    response = requests.get(target)
    soup = BeautifulSoup(response.text, "html.parser") # beautiful soup formats HTML more neatly
    allLinks = soup.find_all("a")  # look for all </a> tags
    # create empty lists to store data later
    results = []
    numbers = []
    emails = []
    for link in allLinks:
        if link.get("href").find("mailto") != -1:  # find email addresses
            emails.append(link.get("href"))  # save to email list
        elif link.get("href").find("@") != -1:  # find email addresses
            emails.append(link.get("href"))  # save to email list
        elif link.get("href").find("tel") != -1:  # find phone numbers
            numbers.append(link.get("href"))  # save to phone number list
        else:
            results.append(link.get("href"))  # save anything not already saved
            recur(target, link.get("href")) # search recursively for more links
    globalresults.append(results)
    globalnumbers.append(numbers)
    globalemails.append(emails)

def Scan(target):
    robots(target)
    URLs(target)
    print(globalresults)
    print(globalnumbers)
    print(globalemails)

target = "http://stemk12.org"
Scan(target)
