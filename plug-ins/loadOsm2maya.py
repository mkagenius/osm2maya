import os, sys

import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
import maya.mel as mel

class osm2mayaTranslator(OpenMayaMPx.MPxFileTranslator):
    description = "osm2maya"

    def __init__(self):
        OpenMayaMPx.MPxFileTranslator.__init__(self)

    def haveWriteMethod(self):
        return True

    def haveReadMethod(self):
        return True

    def filter(self):
        return "*.osm"

    def defaultExtension(self):
        return "osm"

    def writer(self, fileObject, optionString, accessMode):
        pass

    @staticmethod
    def translatorCreator():
        return OpenMayaMPx.asMPxPtr(osm2mayaTranslator())

    def process(self, filepath):
        _argv = {"filepath": filepath}
        pluginPath = mel.eval("pluginInfo -q -p loadOsm2maya;")
        scriptPath = os.path.dirname(os.path.dirname(pluginPath)) + "/osm2maya.py"
        with open(scriptPath, "r") as f:
            src = f.read()

        exec(src, _argv)
         


    def reader(self, fileObject, optionString, accessMode):
        osmfile = fileObject.resolvedFullName()
        self.process(osmfile)



def initializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject, "osm2maya", "1.0")
    try:
        mplugin.registerFileTranslator(osm2mayaTranslator.description, None, osm2mayaTranslator.translatorCreator)
    except:
        sys.stderr.write("Failed to register translator: %s" % osm2mayaTranslator.description)
        raise

def uninitializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.deregisterFileTranslator(osm2mayaTranslator.description)
    except:
        sys.stderr.write("Failed to deregister translator: %s" % osm2mayaTranslator.description)
        raise

