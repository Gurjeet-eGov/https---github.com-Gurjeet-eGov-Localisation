import os
import json
import utils
from pathlib import Path
from payload import LocalizationList

class Localisation:

    SchemaDir: str
    PathList=[]
    FileList=[]
    ModuleList=[]
    MasterList=[]

    LocalisationsList=[]


    def __init__(self, FolderPath):
        uniqueModule = set()
        self.SchemaDir=FolderPath
        obj=os.scandir(path=self.SchemaDir)

        for i in obj:
            if i.is_file():
                #get list of paths
                self.PathList.append(i.path)
                #get list of names
                self.FileList.append(Path(i.path).stem)

        # Gets list of module code and master data code
        for i in self.FileList:
            sliceIndex=i.find('.')
            if i[:sliceIndex] not in uniqueModule:
                uniqueModule.add(i[:sliceIndex].capitalize())
            self.ModuleList=list(uniqueModule)
            self.MasterList.append(i[sliceIndex+1 :].capitalize())
    

    def generateLocalisationArray(self, code,
                                  message, module, locale):
        localization_dict = LocalizationList(
                                code=code,
                                message=message,
                                module=module,
                                locale=locale
                            ).__dict__
        self.LocalisationsList.append(localization_dict)


    def generateLocalisations(self, module, locale):
        
        MasterKeysList=[]
        ModuleName: str
        MasterName: str
        SchemaPrefix="SCHEMA_"
        MasterPrefix="WBH_MDMS_MASTER_"
        ModulePrefix="WBH_MDMS_"

        # Create Module localisations "WBH_MDMS_MASTER_"
        for i in self.ModuleList:
            code = utils.formatCode(prefix=MasterPrefix, code=i)
            self.generateLocalisationArray(code=code, message=i, module=module, locale=locale)
        
        # Creates schema title localisations
        for i in self.PathList:
            
            Index=i.find('/')
            FileName=i[Index+1:].capitalize()
            FileName=FileName.replace('.json', '')
            sliceIndex=FileName.find('.')
            
            # Store module name and master name of current schema def file
            ModuleName=FileName[:sliceIndex].capitalize()
            MasterName=FileName[sliceIndex+1 :].capitalize()
            
            SubPrefix=ModuleName+'_'+MasterName


            # Create Module localisations "WBH_MDMS_"
            code = utils.formatCode(prefix=ModulePrefix, code=ModuleName+'_'+MasterName)
            self.generateLocalisationArray(code=code, message=MasterName, module=module, locale=locale)

            # Create localisations "SCHEMA_MODULENAME_MASTERNAME"
            code=utils.formatCode(prefix=SchemaPrefix, code=SubPrefix)
            self.generateLocalisationArray(code=code, message=MasterName, module=module, locale=locale)



            # Get list of fields within a schema def            
            with open(i) as File:
                jsonData=json.load(File)
                MasterKeysList=utils.extract_properties_keys(jsonData)

            # Create schema fields localisations
            for key in MasterKeysList:
                code=utils.formatCode(prefix=SubPrefix+'_', code=key)
                self.generateLocalisationArray(code=code, message=key, module=module, locale=locale)    
