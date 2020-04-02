import requests
import sys
import time
from bs4 import BeautifulSoup

def Scan(target):
    robots(target)
    URL(target)

def robots(target): #we gonna do a respectful time
    response = requests.get(target + "/robots.txt") #post request to get html
    robotLines = response.text.split("\n") #sort html by line
    disallowed = [] # make empty list to store what's disallowed later
    for i in range(len(robotLines)):
        if robotLines[i].find("Disallow:") >= 0:  #Finding "Disallow:"
            disallowed.append(robotLines[i][10:]) #add to list, minus "Disallow: "
    print(disallowed)

def urlRecur(target, path, sTarget, fname):
    if sTarget.find("http") != -1:
        target2 = sTarget
    elif sTarget.find("www") != -1:
        target2 = sTarget[sTarget.find("www"):len(sTarget)]
        target2 = "https:" + sTarget
    elif sTarget.find("/") != 0:
        target2 = target + "/" + sTarget
    else:
        target2 = target + sTarget + ""
    response = requests.get(target2)
    soup = BeautifulSoup(response.text, "html.parser")
    allLinkTags = soup.find_all("a")
    f = open(path+"/"+fname, "w+")
    if robotsCheck(robotsTXT(target), target2) is False:
        for link in allLinkTags:
            text = str(link.get("href"))
            f.write(text)
            f.write("\n")
            time.sleep(5)


def robotsCheck(robotsDisallowed, target2):
    x = int(0)
    for x in robotsDisallowed:
        if robotsDisallowed[x] == target2:
            return True
    return False


def urlFinder(target):
    response = requests.get(target)
    soup = BeautifulSoup(response.text, "html.parser")
    # ^parse the website into nice-looking html^
    allLinkTags = soup.find_all("a")  # look for all "a" tags
    path = input("Where would you like to save this data? ")
    fname = input("What would you like to call this file? ")
    ftname = input("What would you like to call the telephone number file? ")
    fename = input("What would you like to call the email file? ")
    f = open(path+"/"+fname, "w+")
    ft = open(path+"/"+ftname, "w+")
    fe = open(path+"/"+fename, "w+")
    # ^create or open a file with the user-given names and paths^
    for link in allLinkTags:
        if link.get("href").find("mailto") != -1:  # find email addresses
            fe.write(link.get("href"))  # and write to the email file
            f.write("\n")
            time.sleep(.5)  # wait a little bit
        elif link.get("href").find("@") != -1:  # find email addresses
            fe.write(link.get("href"))  # and write to the email file
            f.write("\n")
            time.sleep(.5)
        elif link.get("href").find("tel") != -1:  # find phone numbers
            ft.write(link.get("href"))  # and write to phone file
            ft.write("\n")
            time.sleep(.5)
        else:
            f.write(link.get("href"))  # find and write links
            f.write(":")
            f.write("\n")
            urlRecur(target, path, link.get("href"), fname)
            # ^recursively do the same thing^
            f.write("\n\n")
    f.close()  # close all the files - good practice
    ft.close()
    fe.close()


def httpCheck(target):  # make sure there's an http in front of the target
    if target.find("http") == -1:
        return "http://" + target
    else:
        return target


# print("Input your target website:")
target = "http://stemk12.org"
urlFinder(target)
