import requests_toolbelt
import Payload.LocalisationUpsert
import Payload.Login
import utils

def LoginPayload():
    configs=utils.get_json("configs.json")
    UserDetails=configs["Superuser"]
    EnvDetails=configs["Environment"]
    Body=Payload.Login.LoginPayload(
                        username=UserDetails["username"], password=UserDetails["password"], 
                        tenantId=EnvDetails["stateCode"], userType=UserDetails["type"]
                    ).__dict__
    Body=requests_toolbelt.MultipartEncoder(fields=Body)
    return Body

def LocalisationUpsertPayload(Token, ReqInfo, LocalisationList):
    configs=utils.get_json("configs.json")
    EnvDetails=configs["Environment"]
    RequestInfo=Payload.LocalisationUpsert.RequestInfo(
                                                apiId="Rainmaker", ver=".01",
                                                ts="", action="_create", did="1",
                                                key="", msgId="20170310130900|en_IN", 
                                                authToken=Token, userInfo=ReqInfo
                                                ).__dict__
    Body=Payload.LocalisationUpsert.LocalisationUpsertBody(RequestInfo=RequestInfo,
                                                    tenantId=EnvDetails["stateCode"],
                                                    messages=LocalisationList).__dict__
    return Body
