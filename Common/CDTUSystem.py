from Common.RSCommon.DLT645.RSCommDLT645Ex import RSCommDLT645Ex
from Common.RSCommon.DLT645.RSFrame645Ex import RSFrame645Ex
import socket
import serial
import asyncio
from .CDTUSystemOption import CDTUSystemOption

class CDTUSystem:
    def __init__(self, option: CDTUSystemOption):
        self.option = option
        self.m_socket = None
        self.m_serial = None
        self.m_did = ""
        self.m_local = True
        self.m_stop = True
        self.m_timeout = None
        self.m_macError = ""

    async def connect_socket(self, host, port):
        self.m_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        await asyncio.wait_for(self.m_socket.connect((host, port)), timeout=self.m_timeout)
        self.m_socket.setblocking(False)

    def connect(self):
        if self.m_serial:
            self.m_serial.close()
            self.m_serial = None

        if self.m_socket:
            self.m_socket.close()
            self.m_socket = None

        self.m_local = self.option.ReadMode != 'DTU_Remote_Read'
        self.m_timeout = self.option.WaitTimeOut_Remote if self.option.ReadMode == 'DTU_Remote_Read' else self.option.WaitTimeOut_Local

        if self.m_local:
            # Assuming SerialMeter is a serial.Serial instance or similar
            self.m_serial = self.option.SerialMeter
            self.m_serial.open()
        else:
            host, port_str = self.option.RemoteHost.split(':')
            port = int(port_str)
            asyncio.run(self.connect_socket(host, port))

    def disconnect(self):
        if self.m_serial:
            self.m_serial.close()
            self.m_serial = None

        if self.m_socket:
            self.m_socket.close()
            self.m_socket = None
    def power(self, meter, flag):
        self.m_stop = False
        self.m_did = meter.DID
        self.m_macError = ""
        if meter.ProtocolType in (0, 1):
            return self.dlt645_comm(meter, flag)

        # The original C# method checks protocol type again and returns False by default
        # It seems like a placeholder for additional conditions or protocols
        return False

    def dlt645_comm(self, meter, flag):

        rsCommDLT645Ex = RSCommDLT645Ex()

        # In Python, we directly assign the method reference instead of using event handlers
        rsCommDLT645Ex.do_mac = self.do_mac
        rsCommDLT645Ex.handle_message = self.handle_message
        rsCommDLT645Ex.attempt_times = self.Option.Attempts
        rsCommDLT645Ex.serial = self.m_serial

        tx_frame = RSFrame645Ex()
        tx_frame.address = meter.MID

        if meter.ProtocolType == 0:
            tx_frame.ctrl_word = 4 if flag in (1, 2) else 1
            if flag == 1:
                tx_frame.data = [61, 192, 0, 102, 102, 102]
            elif flag == 2:
                tx_frame.data = [60, 192, 0, 102, 102, 102]
            else:
                tx_frame.data = [38, 192]
        else:
            tx_frame.ctrl_word = 17

        rs_frame = rsCommDLT645Ex.comm(tx_frame)
        if rs_frame is None:
            meter.ReadResult = 0
            meter.Error = self.m_macError if self.m_macError else "wait timeout"
            return False

        if rs_frame.address != meter.MID:
            meter.Error = "data error"
            meter.ReadResult = 4
            return False

        # The following code is simplified for readability
        # Adjust based on the actual implementation and data structure of RSFrame645Ex
        if flag == 1 and rs_frame.ctrl_word == 132 or flag == 2 and rs_frame.ctrl_word == 132:
            meter.PowerStatus = 1 if flag == 1 else 0
        elif flag not in (1, 2) and rs_frame.ctrl_word == 129:
            binary_str = format(rs_frame.data[2], '08b')
            meter.PowerStatus = 1 if binary_str[4] == '1' and binary_str[7] == '1' else 0
        else:
            meter.Error = "data error"
            meter.ReadResult = 4
            return False

        meter.ReadResult = 1
        return True


# Placeholder for event handlers and classes not defined in the provided code
def do_mac():
    pass


def handle_message():
    pass


