from enum import Enum

class RSMacOperate(Enum):
    Mac_Connect = "MAC层连接"
    Mac_Disconnect = "MAC层断开连接"
    Mac_Send = "MAC发送数据"
    Mac_Receive = "MAC接收数据"
    Mac_Clear = "MAC清除缓存"

class RSMacLayer:
    def __init__(self):
        self.MacError = False
        self.MacOperate = None  # Initially, no operation is set
        self.TxBuf = bytearray()  # Use bytearray for mutable sequences of bytes
        self.RxBuf = bytearray()
