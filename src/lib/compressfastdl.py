# Name: BZ2 Folder Compression
# Author: Braden1996
# Description: This goes through and compresses every file in the source directory
# and saves the result to the output directory. It was designed for use with FastDL
# for the big-booty-bitches.com community

from bz2 import compress
from os import makedirs, walk
from os.path import exists, join, isfile, splitext
from random import randint
from PyQt5.QtCore import QThread
import subprocess

class FastDLFolder():
    """ This class represents a single folder that is to be prepared for FastDL.
        This includes compressing to BZIP2 and generating resource.AddFile(). """
    def __init__(self, statusbar, executeType):
        """ Initiliases our class. """
        self.statusbar = statusbar
        self.validInputs = False  # Internal attribute used to check if inputs are correct
        self.replaceOld = False  # Replace pre-existing zip files
        self.generateResource = True  # Generate resource.AddFile's
        
        # Used to filter the files so we know what to Zip and create resource.AddFile()s
        # If you know any other file-types, let me know!
        self.filter = {"maps": set([".bsp"]),
                        "materials": set([".vmt", ".vtf", ".png"]),
                        "models": set([".vtx", ".mdl", ".phy", ".vvd"]),
                        "sound": set([".mp3", ".wav"]),
                        "particles": set([".pcf"]),
                        "resource": set([".ttf"])}
        
    def sendMessage(self, msg):
        self.statusbar.showMessage(msg)
        
    def setSourceDir(self, newDir):
        """ This is used to set the directory we need compressed. """
        newDir = str(newDir).replace("/", "\\")
        
        if not exists(newDir):
            self.validInputs = False
            return False
        
        self.sourceDir = newDir
        self.validInputs = True

    def setOutputDir(self, newDir):
        """ This is used to set the directory where we put our compressed files. """
        newDir = str(newDir).replace("/", "\\")
        if newDir[-1:] != "\\":
            newDir += "\\"
                
        if not exists(newDir):
            makedirs(newDir)

        self.outputDir = newDir

    def cropPath(self, path):
        """ Crops out the unneeded parts of the given path. Returns False if all invalid. """
        dirList = path.split("\\")
        for i in range(len(dirList)):
            if dirList[0] in self.filter:
                if splitext(path)[1] in self.filter[dirList[0]]:
                    return "\\".join(dirList), "\\".join(dirList[0:len(dirList)-1]) + "\\"
                else:
                    return False, False
            else:
                dirList.pop(0)
        return False, False
        
    def runCompression(self):
        """ This executes the compression process. """
        if not self.validInputs:
            if hasattr(self, "sourceDir") and type(self.sourceDir) == "string":
                self.sendMessage("You cannot compress the folder '(" + self.sourceDir + ")' as it doesn't exist!")
            else:
                self.sendMessage("You have not entered a source directory, or it of an invalid type!")
            return False

        count = 0
        if self.generateResource: self.resourceStr = "if (SERVER) then"
        for root, dirs, files in walk(self.sourceDir):
            for curFile in files:
                path = join(root, curFile)
                cropPath, cropRoot = self.cropPath(path)
                if not cropPath:
                    continue
                with open(path, "rb") as fileObj:
                    if not exists(join(self.outputDir, cropRoot)):
                        makedirs(join(self.outputDir, cropRoot))

                    bz2Path = join(self.outputDir, cropPath)
                    if self.replaceOld or not (isfile(bz2Path) or isfile(bz2Path + ".bz2")):
                            if self.generateResource: self.resourceStr += "\n\tresource.AddSingleFile(\"" + cropPath.replace("\\", "/") + "\")"
                            fileObjContent = fileObj.read()
                            bz2ObjContent = compress(fileObjContent)
                            if len(bz2ObjContent) > fileObj.tell():
                                with open(bz2Path, "wb") as newFileObj:
                                    newFileObj.write(fileObjContent)
                            else:
                                with open(bz2Path + ".bz2", "wb") as bz2FileObj:
                                    bz2FileObj.write(bz2ObjContent)
                            count += 1
        output = "Finished! We compressed '" + str(count) + "' files!"

        if self.generateResource and count > 0:
            self.resourceStr += "\nend"
            with open(join(self.outputDir, "fastdl_" + str(randint(1, 9999)) + ".lua"), "w") as resourceFileObj: resourceFileObj.write(self.resourceStr)
            output += " Your resource file was also generated!"

        self.sendMessage(output)

    def unpackGma(self):
        """ This scans for .gma files and unpacks them. """
        if not self.validInputs:
            if hasattr(self, "sourceDir") and type(self.sourceDir) == "string":
                self.sendMessage("You cannot compress the folder '(" + self.sourceDir + ")' as it doesn't exist!")
            else:
                self.sendMessage("You have not entered a source directory, or it of an invalid type!")
            return False

        if not exists(self.outputDir):
            makedirs(self.outputDir)

        count = 0
        for root, dirs, files in walk(self.sourceDir):
            for curFile in files:
                path = join(root, curFile)
                if splitext(path)[1] == ".gma":
                    printPath = path.split("\\")
                    self.sendMessage("Unpacking: '" + printPath[len(printPath)-1] + "'")
                    p = subprocess.Popen(["lib/gmadconv.exe", path], cwd=self.outputDir)
                    p.wait()
                    count += 1
        self.sendMessage("Finished! We unpacked '" + str(count) + "' .gma files!")
