#!/usr/bin/env python

"""populate_wxs.py: Script to create file and directory tags for the Endless Sky WiX installer file."""

__author__ = "capnchainsaw"

from os import listdir
from os.path import basename, isdir, isfile, join
from uuid import uuid4

def CreateFileComponentRef(path, directoryName, directoryStr, componentIds, tabdepth):
    """Create File tags within a Component tag for files in directory."""
    componentId = "%sFiles" % (directoryName)
    directoryComponentStr = "%s<Component Id=\"%s\" Guid=\"%s\">\n" % (tabdepth, componentId, uuid4())
    fileCount = 0
    for f in listdir(path):
        filepath = join(path, f)
        if isfile(filepath):
            scrubbedName = f.replace(".","").replace("-","").replace("+","").replace("_","").replace(" ","").replace("~","").replace("=","")
            directoryComponentStr += "%s<File Id=\"%s%s\" Source=\"%s\" />\n" % (tabdepth + "    ", directoryName, scrubbedName, filepath)
            fileCount += 1
    directoryComponentStr += "%s</Component>\n" % (tabdepth)
    if fileCount > 1:
        directoryStr += directoryComponentStr
        componentIds.append(componentId)
    return directoryStr, componentIds

def CreateDirectoryRef(path, directoryName, directoryStr, componentIds, tabdepth):
    directoryStr += "%s<Directory Id=\"%sDir\" Name=\"%s\">\n" % (tabdepth, directoryName, directoryName)
    subtabdepth = tabdepth + "    "
    
    directoryStr, componentIds = CreateFileComponentRef(path, directoryName, directoryStr, componentIds, subtabdepth)
    
    # Create Directory tags for sub-directories.
    for f in listdir(path):
        subpath = join(path, f)
        if isdir(subpath):
            directoryStr, componentIds = CreateDirectoryRef(subpath, f.replace(" ",""), directoryStr, componentIds, subtabdepth)
    
    directoryStr += "%s</Directory>\n" % (tabdepth)
    return directoryStr, componentIds

directoryStr = ""
componentIds = []
tabdepth = "			  "

# Create strings to populate template.
directoryStr, componentIds = CreateFileComponentRef("..\\bin\\Release", "Application", directoryStr, componentIds, tabdepth)
directoryStr, componentIds = CreateDirectoryRef("..\\data", "data", directoryStr, componentIds, tabdepth)
directoryStr, componentIds = CreateDirectoryRef("..\\images", "images", directoryStr, componentIds, tabdepth)
directoryStr, componentIds = CreateDirectoryRef("..\\sounds", "sounds", directoryStr, componentIds, tabdepth)

componentStr = ""
for componentId in componentIds:
    componentStr += "        <ComponentRef Id=\"%s\"/>\n" % (componentId)

# Read template and populate.
templateFile = open("EndlessSky.wxs.tmpl", "r")
wxsString = templateFile.read()
wxsString = wxsString.replace("${INSTALLFILES}", directoryStr)
wxsString = wxsString.replace("${COMPONENTIDS}", componentStr)

# Write out WiX file.
wxsFile = open("EndlessSky.wxs", "w")
wxsFile.write(wxsString)
wxsFile.close()
