from typing import List, Tuple, Optional

from Common.RSCommon.RSTools import RSTools


class RSFrame645Ex:
    def __init__(self):
        self.m_address = '000000000000'
        self.CtrlWord = 0
        self.Data = bytearray()
        self.FrameBuffer = bytearray()
        self.CSError = False

    @property
    def Address(self):
        return self.m_address

    @Address.setter
    def Address(self, value: str):
        self.m_address = value.zfill(12)[:12]

    def GetFrameLen(self) -> int:
        return len(self.Data) + 12

    def PickFrame(self, src: bytearray) -> int:
        num = len(src)
        if num < 12:
            return -1

        num2 = -1
        for i in range(num):
            if src[i] == 104 and num >= i + 12 and src[i + 7] == 104 and num >= src[i + 9] + 12 + i and src[i + src[i + 9] + 11] == 22:
                self.CSError = RSTools.calc_cs(src, i, src[i + 9] + 10) != src[i + src[i + 9] + 10]
                num2 = i
                break

        if num2 == -1:
            return -1

        address_bytes = src[num2+1:num2+7]
        self.Address = ''.join(f'{b:02X}' for b in reversed(address_bytes))
        self.CtrlWord = src[num2 + 8]
        num3 = src[num2 + 9]
        self.Data = bytearray([src[10 + j + num2] - 51 for j in range(num3)])
        self.FrameBuffer = src[num2:num2 + num3 + 12]
        return num2

    def BuildFrame(self) -> bytearray:
        frame_len = self.GetFrameLen()
        self.FrameBuffer = bytearray(frame_len)
        self.FrameBuffer[0] = 104
        address_bytes = [int(self.Address[10-2*i:12-2*i], 16) for i in reversed(range(6))]
        self.FrameBuffer[1:7] = bytearray(address_bytes)
        self.FrameBuffer[7] = 104
        self.FrameBuffer[8] = self.CtrlWord
        self.FrameBuffer[9] = len(self.Data)
        for i, d in enumerate(self.Data):
            self.FrameBuffer[10 + i] = d + 51
        self.FrameBuffer[-2] = RSTools.calc_cs(self.FrameBuffer, 0, frame_len - 2)
        self.FrameBuffer[-1] = 22
        return self.FrameBuffer

    def GetDataString(self) -> str:
        return RSTools.ByteArrayToHexStr(self.Data, 0, len(self.Data))

    def GetFrameString(self) -> str:
        return RSTools.ByteArrayToHexStr(self.FrameBuffer, 0, len(self.FrameBuffer))

    def GetFrameStringSub33(self) -> str:
        array = bytearray(len(self.FrameBuffer))
        array[:] = self.FrameBuffer[:]
        for i in range(array[9]):
            array[10 + i] = self.Data[i]
        return RSTools.ByteArrayToHexStr(array, 0, len(array))

    @staticmethod
    def try_parse(src: bytearray) -> Tuple[bool, Optional['RSFrame645Ex']]:
        frame = RSFrame645Ex()
        index = frame.PickFrame(src)
        if index >= 0:
            return True, frame
        return False, None