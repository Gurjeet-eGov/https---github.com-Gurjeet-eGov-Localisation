"""egov-user request dataclass"""
from dataclasses import dataclass
from typing import List,Optional

@dataclass
class Localization:
    code: str
    message: str
    module: str
    locale: str