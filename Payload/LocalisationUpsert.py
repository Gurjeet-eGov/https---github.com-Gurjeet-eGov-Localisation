"""egov-user request dataclass"""
from dataclasses import dataclass, field
from typing import List,Optional

@dataclass
class Role:
    name: str
    code: str
    tenantId: str

@dataclass
class UserInfo:
    id: int
    uuid: str
    userName: str
    name: str
    mobileNumber: str
    emailId: Optional[str]
    locale: Optional[str]
    type: str
    roles: List[Role]
    active: bool
    tenantId: str
    permanentCity: Optional[str]

@dataclass
class RequestInfo:
    apiId: str
    ver: str
    ts: str
    action: str
    did: str
    key: str
    msgId: str
    authToken: str
    userInfo: UserInfo

@dataclass
class LocalizationList:
    code: str
    message: str
    module: str
    locale: str

@dataclass
class LocalisationUpsertBody:
    RequestInfo: RequestInfo
    tenantId: str
    messages: List[LocalizationList]
