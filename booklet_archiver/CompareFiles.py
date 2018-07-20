import os, hashlib, datetime

def main():

    print("Start of main")

    oldFilesDir = ""
    newFilesDir = ""

    oldFiles = getAllFiles("pdf_1")
    newFiles = getAllFiles("pdf_2")

    results = compareAllFiles(oldFiles, newFiles)

    writeResultToTextFile("log.txt", results)

def writeResultToTextFile(logFile, results):

    with open(logFile, 'a') as f:
        time = datetime.datetime.now().time()
        f.write("\n")
        for line in results:
            f.write(line+"\n")
        f.write("The log section was written at: " + str(time) + ".\n")

def getAllFiles(directory):

    filePaths = []
    for (dirpath, dirnames, filenames) in os.walk(directory):
        for f in filenames:
            if f != ".DS_Store":
                filePaths.append(os.path.join(dirpath, f))

    return filePaths

def compareAllFiles(oldFiles, newFiles):
    
    changedFilesLog = []

    dirSeperator = "/"
    # Remove top file name from path for comparison
    oldDict = {}
    for path in oldFiles:
        shortPath = dirSeperator.join(path.split(dirSeperator)[1:])
        oldDict[shortPath] = path

    newDict = {}
    for path in newFiles:
        shortPath = dirSeperator.join(path.split(dirSeperator)[1:])
        newDict[shortPath] = path

    for filePath in newFiles:
        shortPathName = dirSeperator.join(filePath.split(dirSeperator)[1:])
        # Check if file exists and compare hash
        # print(filePath)
        # print(shortPathName)

        if oldDict.get(shortPathName) != None:
            # Compare hash of files
            if getFileHash(filePath) == getFileHash(oldDict.get(shortPathName)):
                pass
            else:
                messege = "File located at %s, is present but has a different hash to the previous match." % filePath
                changedFilesLog.append(messege)
        else:
            messege = "File located at %s, is not present in the old files set." % filePath
            changedFilesLog.append(messege)
        # print()
    
    # Check if file has been removed
    for filePath in oldFiles:
        shortPath = dirSeperator.join(filePath.split(dirSeperator)[1:])
        if newDict.get(shortPath) == None:
            messege = "File located at %s, is no longer present in the new download." % filePath
            changedFilesLog.append(messege)

    print(changedFilesLog)
    return changedFilesLog

def getFileHash(filePath):

    with open(filePath, 'rb') as f:
        contents = f.read()
        return hashlib.sha256(contents).hexdigest()

if __name__ == "__main__":
    print('start')
    
    main()