from enum import Enum

class CDTUSystem_ReadMode(Enum):
    Local_Read = 1  # Local serial reading meter
    DTU_Remote_Read = 2  # Remote DTU reading meter