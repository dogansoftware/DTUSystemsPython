
class RSMacLayer:
    def __init__(self):
        self.MacError = False
        self.MacOperate = None  # Initially, no operation is set
        self.TxBuf = bytearray()  # Use bytearray for mutable sequences of bytes
        self.RxBuf = bytearray()
