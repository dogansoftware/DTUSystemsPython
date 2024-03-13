import threading

from typing import List

from Common.RSCommon import RSTools
from Common.RSCommon.RSMacLayer import RSMacLayer
from Common.RSCommon.Serial.RSSerial import RSSerial


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
    def Address(self, value):
        self.m_address = value.zfill(12)

    def GetFrameLen(self):
        return len(self.Data) + 12

    def PickFrame(self, src):
        num = len(src)
        if num < 12:
            return -1

        num2 = -1
        for i in range(num):
            if src[i] != 104 or num < i + 12 or src[i + 7] != 104 or num < src[i + 9] + 12 + i:
                continue
            if src[i + src[i + 9] + 11] == 22:
                self.CSError = False
                if RSTools.CalcCS(src, i, src[i + 9] + 10) != src[i + src[i + 9] + 10]:
                    self.CSError = True

                num2 = i
                break

        if num2 == -1:
            return -1

        self.Address = ''.join([f"{src[num2 + 6 - j]:X2}" for j in range(6)])
        self.CtrlWord = src[num2 + 8]
        num3 = src[num2 + 9]
        self.Data = bytearray(num3)
        for j in range(num3):
            self.Data[j] = src[10 + j + num2] - 51

        self.FrameBuffer = src[num2:num2 + num3 + 12]
        return num2

    def BuildFrame(self):
        frame_len = self.GetFrameLen()
        self.FrameBuffer = bytearray(frame_len)
        self.FrameBuffer[0] = 104
        address_bytes = [int(self.Address[i:i+2], 16) for i in range(0, len(self.Address), 2)]
        self.FrameBuffer[1:7] = bytearray(address_bytes[::-1])
        self.FrameBuffer[7] = 104
        self.FrameBuffer[8] = self.CtrlWord
        self.FrameBuffer[9] = len(self.Data)
        self.FrameBuffer[10:10+len(self.Data)] = bytearray([d + 51 for d in self.Data])
        self.FrameBuffer[-2] = RSTools.CalcCS(self.FrameBuffer, 0, frame_len - 2)
        self.FrameBuffer[-1] = 22
        return self.FrameBuffer

    # Assume GetDataString and GetFrameString methods are similar to the C# version, using a hypothetical RSTools for conversions.

# Placeholder for RSTools functions, implement as needed


