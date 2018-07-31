import os, hashlib, datetime
from difflib import SequenceMatcher

def compareOldestTwoFilesTrees(saveDirectory):

    files = [f for f in os.listdir(saveDirectory) if f[0] != "."]
    
    if len(files) <= 1:
        print("Only one file tree was found. Cannot run comparison.")
        return

    files.sort()
    newFilesDir = saveDirectory + files[-1]
    oldFilesDir = saveDirectory + files[-2]


    # print(files, oldFilesDir, newFilesDir)
    oldFiles = getAllFiles(oldFilesDir)
    newFiles = getAllFiles(newFilesDir)

    results = compareAllFiles(oldFiles, newFiles)

    writeResultToTextFile("log.txt", results)

def writeResultToTextFile(logFile, results):

    with open(logFile, 'a') as f:
        time = datetime.datetime.now().time()
        f.write("\n")
        for line in results:
            f.write(line+"\n")
        if len(results) == 0:
            f.write("No changes were found.\n")
        f.write("The log section was written at: " + str(time) + ".\n")

def getAllFiles(directory):

    filePaths = []
    for (dirpath, dirnames, filenames) in os.walk(directory):
        for f in filenames:
            if f != ".DS_Store":
                filePaths.append(os.path.join(dirpath, f))

    return filePaths

def getShortDirName(path, dirSeperator="/", fileDepth = 2):
    return dirSeperator.join(path.split(dirSeperator)[fileDepth:])

def buildFileNameToFilePathDict(files, fileDepth=2):
    # Remove top file name from path for comparison
    data = {}
    for path in files:
        shortPath = getShortDirName(path, fileDepth=2)
        data[shortPath] = path
    return data

def compareAllFiles(oldFiles, newFiles):
    
    changedFilesLog = []

    oldDict = buildFileNameToFilePathDict(oldFiles)
    newDict = buildFileNameToFilePathDict(newFiles)

    for filePath in newFiles:
        shortPathName = getShortDirName(filePath)
        # Check if file exists and compare hash
        # print(filePath)
        # print(shortPathName)

        if oldDict.get(shortPathName) != None:
            # Compare hash of files
            oldFildPath = oldDict.get(shortPathName)
            if getFileHash(filePath) == getFileHash(oldFildPath):
                pass
            else:
                text1 = open(filePath,"rb").read()
                text2 = open(oldFildPath,"rb").read()
                m = SequenceMatcher(None, text1, text2)
                diffRatio = 1 - m.quick_ratio()
                messege = "File located at %s, is present but has a different hash to the previous match. Ratio of diff is %s" % (filePath, str(diffRatio))
                changedFilesLog.append(messege)
        else:
            messege = "File located at %s, is not present in the old files set." % filePath
            changedFilesLog.append(messege)
        # print()
    
    # Check if file has been removed
    for filePath in oldFiles:
        shortPath = getShortDirName(filePath)
        if newDict.get(shortPath) == None:
            messege = "File located at %s, is no longer present in the new download." % filePath
            changedFilesLog.append(messege)

    # print(changedFilesLog)
    return changedFilesLog

def getFileHash(filePath):

    with open(filePath, 'rb') as f:
        contents = f.read()
        return hashlib.sha256(contents).hexdigest()

if __name__ == "__main__":
    print('start')
    
    main()