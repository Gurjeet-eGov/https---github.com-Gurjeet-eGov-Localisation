import utils
import requests
import requests_toolbelt
import json
import PayloadBuilder
from Payload import Login


configs=utils.get_json("configs.json")
endpoints=utils.get_json("endpoints.json")
UserDetails=configs["Superuser"]
EnvDetails=configs["Environment"]
URL=EnvDetails["host"]

def LoginAPI():
    API=endpoints["Login"]
    Body=PayloadBuilder.LoginPayload()
    Headers=EnvDetails["auth_header"]
    Headers['content-type']=Body.content_type

    Response=requests.post(
                            url=URL+API["oauth"], 
                            headers=Headers, 
                            data=Body
                            )

    access_token=Response.json()['access_token']
    UserRequest=Response.json()['UserRequest']

    return access_token, UserRequest


def LocalisationUpsert(Token, ReqInfo, LocalisationList):
    API=endpoints["Localisation"]
    Body=PayloadBuilder.LocalisationUpsertPayload(Token=Token, 
                                              ReqInfo=ReqInfo,
                                              LocalisationList=LocalisationList
                                              )


    Response=requests.post(
                            url=URL+API["upsert"],
                            json=Body
                            )
    
    return Response