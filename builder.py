import os
import json
import re
import time

version = [0,1,1,0]
# to do:
# - automatically choosing json if there's only 1 in the working directory [0.1.2.0]
# - version compatibility check [0.1.3.0]
# - update IGM to JSON conversion (its missing repts, version, and a couple more im not thinking of) [0.1.4.0]
# - addition of vect (triple loop, x/y/z) and grid (double loop, x/y) [0.2.0.0]
# - adding an ifs statement to the builder.py eval systen [1.0.0.0]
# - convert text with builder.py debug comments to build.json [1.0.1.0]
# - advanced debug comments generator [1.0.2.0]
# - provide txt to txt conversion with options for enabling or disabling debug comments [1.0.3.0]
# - create helper scripts to automatically generate new game files without configuration [1.0.4.0]

# versions before versions were written
# - MVP, order items wasn't a list with key and optional rept, and there were titles for blocks (and items automatically had tab indentations added) [-1.0.1.0]
# - got rid of titles for blocks, and now tab indentations were manual [-1.1.0.0]
# - added debug comments, and created the igm txt (with said comments) to json converter [0.0.0.0]
# - added dot and line repetition, as well as the whole eval system (crazy work me) [0.1.0.0]
# - - fun fact: the above update was initially 1.0.0.0 until i realized i had a *long way to go* :sigh:
# - changed the json path selection to not automatically use the build.json in current work directory, as well as moved the txt path selection to the json [0.1.1.0]

def findBuildJSON():
    cwd = os.getcwd()
    fileList = os.listdir(cwd)
    jsonRegex = re.compile(".+\\.json")
    jsonList = []
    for i in fileList:
        matchForJSON = jsonRegex.match(i)
        if matchForJSON != None:
            matches = matchForJSON.group()
            jsonList.append(matches)
            print("| "+str(matches))
    print("Choose between the above options of JSON file in your, or direct to a different JSON file in your computer [A].")
    fileOpt = input("> ")
    if fileOpt == "A":
        pathOpt = input("Please choose the JSON file to point to or cancel the operation [N]. ")
        if pathOpt == "N":
            return False
        else:
            filePath = os.path.join(cwd,pathOpt)
    else:
        for i in jsonList:
            if fileOpt.find(i) != -1:
                filePath = os.path.join(cwd,fileOpt)
                buildJSON = open(filePath)
                buildList = json.load(buildJSON)
                return buildList
    return False
def askBuildJSON():
    print("something should happen here")
def getPath():
    cwd = os.getcwd()
    fileList = os.listdir(cwd)
    for i in fileList:
        if i=="game.txt":
            print("Found existing game.txt in working directory!")
            confirm = input("Choose to override [0], save as a new file [1], or cancel operation [2] ")
            if confirm=="0":
                return os.path.join(cwd,"game.txt")
            elif confirm=="1":
                newFilePath = input("Please enter new file path here: ")
                return newFilePath
            elif confirm=="2":
                return False
    print("Saving file in game.txt in working directory due to lack of file options in build instructions!")
    return [cwd,"game.txt"]
def createNewTXT(json):
    gameStr = "Let's make a game!\n"
    expressionRegex = re.compile("{(?!\\/)([^>]+?)}")
    skippedExpRegex = re.compile("{(?:\\/)(.+?)}")
    for i in json["order"]:
        try:
            mode = json["order"][i]["rept"]["mode"]
        except:
            mode = "blank"
        match mode:
            case "dot":
                x = 0
                repts = int(json["order"][i]["rept"]["size"])
                while x!= repts:
                    if repts == 1:
                        gameStr += "// builder.py automatic debug: line is start of block \""+block+"\"\n"
                    elif repts == 2:
                        gameStr += "// builder.py automatic debug: repeated lines below"
                    block = json["order"][i]["key"]
                    for i2 in json["items"][block]:
                        prepStr = json["items"][block][i2]+"\n"
                        prepStr = expressionRegex.sub(procExp,prepStr)
                        gameStr += skippedExpRegex.sub(lambda m: "{"+m.group(1)+"}",prepStr)
                    x += 1
            case "line":
                x = 0
                repts = int(json["order"][i]["rept"]["size"])
                while x!= repts:
                    if repts == 1:
                        gameStr += "// builder.py automatic debug: line is start of block \""+block+"\"\n"
                    elif repts == 2:
                        gameStr += "// builder.py automatic debug: repeated lines below"
                    block = json["order"][i]["key"]
                    for i2 in json["items"][block]:
                        prepStr = json["items"][block][i2]+"\n"
                        prepStr = expressionRegex.sub(lambda m: procExp(m,x+1),prepStr)
                        gameStr += skippedExpRegex.sub(lambda m: "{"+m.group(1)+"}",prepStr)
                    x += 1
            case _:
                block = json["order"][i]["key"]
                for i2 in json["items"][block]:
                    prepStr = json["items"][block][i2]+"\n"
                    prepStr = expressionRegex.sub(procExp,prepStr)
                    gameStr += skippedExpRegex.sub(lambda m: "{"+m.group(1)+"}",prepStr)
    try:
        if json["export"]["dir"] == "cwd":
            dirPath = os.getcwd()
        else:
            dirPath = json["export"]["dir"]
        filePath = json["export"]["file"]
    except:
        pathList = getPath()
        dirPath = pathList[0]
        filePath = pathList[1]
    path = os.path.join(dirPath,filePath)
    with open(path, 'w') as file:
        file.write(gameStr)
    print("Game built at "+path+"!")
def procExp(matchobj, *args):
    for ar in args:
        count = 1
        match count:
            case 1:
                x = ar
            case 2:
                y = ar
            case 3:
                z = ar
        count += 1
    exp = matchobj.group(1)
    validRegex = re.compile("[\\-+*/%0-9x-z]+")
    validExp = validRegex.findall(exp)
    for char in validExp:
        newExp = ""
        newExp += char
    return str(eval(newExp))
def createBuild(txt):
    cwd = os.getcwd()
    fileList = os.listdir(cwd)
    for i in fileList:
        if i=="build.json":
            print("Found existing build.json in working directory!")
            confirm = input("Choose to override [0], save to a new file [1], or cancel operation [2] ")
            if confirm=="0":
                createBuildJSON(txt, os.path.join(cwd,"build.json"))
                return True
            elif confirm=="1":
                newFilePath = input("Please enter new file path here: ")
                createBuildJSON(txt, newFilePath)
                return True
            elif confirm=="2":
                return False
def createBuildJSON(txt,path):
    jsonDict = {"order": {}, "items": {}}
    txtFile = open(txt)
    fileLines = txtFile.readlines()
    x = 1
    y = 1
    z = 0
    for line in fileLines:
        debugAdvValid = re.compile("// builder.py automatic debug: line is start of block \"(.+)\" with data \"(.+)\"")
        debugValid = re.compile("// builder.py automatic debug: line is start of block \"(.+)\"")
        if debugAdvValid.match(line) != None:
            m = debugAdvValid.match(line)
        elif debugValid.match(line) != None:
            m = debugValid.match(line)
        if m != None:
            z += 1
            jsonDict["order"][z] = {}
            jsonDict["order"][z]["key"] = m.group(1)
            jsonDict["order"][z]["repeat"] = m.group(2)
            jsonDict["items"][jsonDict["order"][z]] = {}
            y = 1
        elif x == 1 or x == "":
            pass
        else:
            fmrLine = line.replace("\n","")
            jsonDict["items"][jsonDict["order"][z]][y] = fmrLine
            y += 1
        x += 1
    jsonB = json.dumps(jsonDict, indent=4)
    with open(path, 'w') as file:
        file.write(jsonB)
    print("Build instructions built at "+path+"!")
def getText():
    cwd = os.getcwd()
    fileList = os.listdir(cwd)
    for i in fileList:
        if i=="game.txt":
            txtExists = True
    inputStr = ""
    if txtExists == True:
        inputStr += "Use existing game.txt in working directory [1], different file [2], or cancel the operation [N]? "
    else:
        inputStr += "Please put in your file path or put in [N] to cancel. "
    userInput = input(inputStr)
    if txtExists == True and userInput == "1":
        return os.path.join(cwd,"game.txt")
    elif txtExists == True and userInput == "N":
        return False
    else:
        if txtExists == True:
            inputPath = input("Please put in your file path or put in [N] to cancel. ")
        else:
            inputPath == userInput
        if inputPath == "N":
            return False
        else:
            return os.path.join(cwd,inputPath)
    return False

print("Welcome to builder.py, the only IGM compiler that has ever (and should ever) exist.")
time.sleep(1)
askFunc = input("Press [0] to convert JSON to IGM, and press [1] to convert IGM to JSON. ")
if askFunc == "0":
    buildJSON = findBuildJSON()
    if buildJSON==False:
        askBuildJSON()
    else:
        createNewTXT(buildJSON)
elif askFunc == "1":
    gameText = getText()
    createBuild(gameText)
