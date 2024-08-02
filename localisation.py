import os
from pathlib import Path
import json

class Localisation:

    SchemaDir: str
    PathList=[]
    FileList=[]
    moduleName=[]
    masterDataName=[]

    def __init__(self, FolderPath):
        self.SchemaDir=FolderPath
        obj=os.scandir(path=self.SchemaDir)

        for i in obj:
            if i.is_file():
                #get list of paths
                self.PathList.append(i.path)
                #get list of names
                self.FileList.append(Path(i.path).stem)

    def codeGen(self):
        
        for i in self.FileList:
            sliceIndex=i.find('.')
            self.moduleName.append(i[:sliceIndex])
            self.masterDataName.append(i[sliceIndex+1 :])

    def getJsonData(self):
        jsonData={}
        for file in self.PathList:
            if file=="schemaDefs/PropertyTax.UsageCategoryMinor.json":
                with open(file) as File:
                    jsonData=json.load(File)
                print(list(jsonData['properties'].keys()))

    def generateLocJson(self):
        pass