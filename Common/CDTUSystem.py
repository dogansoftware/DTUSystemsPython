from Common.RSCommon.DLT645.RSCommDLT645Ex import RSCommDLT645Ex
from Common.RSCommon.DLT645.RSFrame645Ex import RSFrame645Ex
import socket
import serial
import asyncio
from .CDTUSystemOption import CDTUSystemOption
from .CDTUSystemReadMode import CDTUSystemReadMode
from .RSCommon.RSMacLayer import RSMacLayer, RSMacOperate
from enum import Enum


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
        # Create a non-blocking socket using asyncio's loop
        self.m_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.m_socket.setblocking(False)  # Set socket to non-blocking mode

        # Get the current event loop
        loop = asyncio.get_running_loop()

        # Wait for the socket to connect
        await loop.sock_connect(self.m_socket, (host, port))

    def connect(self):
        if self.m_serial:
            self.m_serial.close()
            self.m_serial = None

        if self.m_socket:
            self.m_socket.close()
            self.m_socket = None

        self.m_local = self.option.ReadMode != CDTUSystemReadMode.DTU_Remote_Read
        self.m_timeout = self.option.WaitTimeOut_Remote if self.option.ReadMode == CDTUSystemReadMode.DTU_Remote_Read else self.option.WaitTimeOut_Local

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
        rsCommDLT645Ex.attempt_times = self.option.Attempts
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
    def handle_message(self, sender, event_args):
        # Perform the necessary event handling logic here
        print("Event handled")

    def do_mac(self, sender, mac):
        if mac.MacOperate == RSMacOperate.Mac_Send:
            self.mac_send(mac.TxBuf)
        elif mac.MacOperate == RSMacOperate.Mac_Receive:
            mac.RxBuf = self.mac_recv()
            if self.m_macError:  # Checking if m_macError has a truthy value
                mac.MacError = True
        elif mac.MacOperate == RSMacOperate.Mac_Clear:
            if self.m_local:
                self.m_serial.reset_input_buffer()  # Assuming m_serial is a pySerial Serial object
            else:
                self.m_socket.clear_available()  # This method needs to be implemented in your socket handling class

    async def mac_recv(self):
        if self.m_local:
            bytes_to_read = self.m_serial.in_waiting  # BytesToRead equivalent in pySerial
            if bytes_to_read <= 0:
                return None
            buffer = self.m_serial.read(bytes_to_read)
            return buffer
        else:
            # Assuming m_socket has a WaitForData method implemented,
            # you would need to adapt it for Python. This is a placeholder
            # for whatever method you use to receive data from the socket.
            data = await self.m_socket.wait_for_data()  # This method needs to be implemented based on your socket handling
            if data is None:
                return None
            num = len(data)
            count = data[17] * 256 + data[18]
            array = data[19:19+count]
            if count == 9 and array.decode("utf-8") == "No Online":
                self.m_macError = "DTU No Online"
                return None
            elif count == 7 and array.decode("utf-8") == "DTU Busy":
                self.m_macError = "DTU Busy"
                return None
            return array





