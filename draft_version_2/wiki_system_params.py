"""parameters to change the wiki at  system/arch level
"""
from aenum import Enum

class StorageType(Enum):
    sqlite = "sqlite"
    fs = "fs"
