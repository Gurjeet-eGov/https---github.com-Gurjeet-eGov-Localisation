import RequestsCaller
from localisation import *

loc_obj=Localisation(FolderPath="SchemaDefs")
loc_obj.generateLocalisations(module="rainmaker-workbench", locale="en_IN")

LoginResponse=RequestsCaller.LoginAPI()
Token=LoginResponse[0]
UserReqInfo=LoginResponse[1]

Localisations=loc_obj.LocalisationsList

print("token: ", Token, "\nReq Info: ", UserReqInfo)

LocalisationResponse=RequestsCaller.LocalisationUpsert(Token=Token,
                                                       ReqInfo=UserReqInfo,
                                                       LocalisationList=Localisations)
print(LocalisationResponse.status_code)

with open('response.json', 'w') as file:
    file.write(json.dumps(LocalisationResponse.json()))