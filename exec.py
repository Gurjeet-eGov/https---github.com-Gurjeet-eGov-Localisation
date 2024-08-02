from localisation import Localisation

loc_obj=Localisation(FolderPath="schemaDefs")

print(loc_obj.FileList)

loc_obj.codeGen()

print(loc_obj.masterDataName)
print(loc_obj.moduleName)