"""egov-user request dataclass"""
from dataclasses import dataclass
from typing import List,Optional

@dataclass
class LocalizationList:
    code: str
    message: str
    module: str
    locale: str