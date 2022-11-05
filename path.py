import os.path

#Permite acceder a los assets de manera sencilla usando el módulo os.path.
def getAssetPath(filename):
    thisFilePath = os.path.abspath(__file__)
    thisFolderPath = os.path.dirname(thisFilePath)
    assetsDirectory = os.path.join(thisFolderPath, "assets")
    requestedPath = os.path.join(assetsDirectory, filename)
    return requestedPath

#Permite acceder a las instrucciones de manera sencilla usando el módulo os.path.
def getInstructionPath(filename):
    thisFilePath = os.path.abspath(__file__)
    thisFolderPath = os.path.dirname(thisFilePath)
    assetsDirectory = os.path.join(thisFolderPath, "instructions")
    requestedPath = os.path.join(assetsDirectory, filename)
    return requestedPath