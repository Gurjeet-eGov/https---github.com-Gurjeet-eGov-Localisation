import json
from localisation import Localisation

loc_obj=Localisation(FolderPath="schemaDefs")

loc_obj.generateLocalisations(module="rainmaker-workbench", locale="en_IN")

print(json.dumps(loc_obj.LocalisationsList))