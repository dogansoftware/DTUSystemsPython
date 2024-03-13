from Common.RSCommon.DLT645.RSFrame645Ex import RSFrame645Ex
from Common.RSCommon.RSMacLayer import RSMacLayer
from Common.RSCommon.Serial.RSSerial import RSSerial


class RSCommDLT645Ex:
    def __init__(self):
        self.BUFFER_SIZE = 1024
        self.m_stop = False
        self.m_auto = False
        self.m_mac = RSMacLayer()
        self.m_rx = bytearray()
        self.Serial = RSSerial()
        self.Serial.baudrate = 9600
        self.Serial.data_received_callback = self.on_serial_comm
        self.WaitTimeout = 5000
        self.AutoReceive = False
        self.AttemptTimes = 1
        self.HandleMessage = None
        self.DoMac = None
        self.OnReceive = None

    def mac_recv(self):
        if self.DoMac is not None:
            self.m_mac.mac_operate = RSMacLayer.RSMacOperate.Mac_Receive
            self.m_mac.mac_error = False
            self.DoMac(self, self.m_mac)
            return self.m_mac.rxbuff

        bytes_to_read = self.Serial.bytes_to_read()
        if bytes_to_read <= 0:
            return bytearray()

        array = self.Serial.read(bytes_to_read)
        return array

    def mac_send(self, buf):
        if self.DoMac is not None:
            self.m_mac.mac_operate = RSMacLayer.RSMacOperate.Mac_Send
            self.m_mac.mac_error = False
            self.m_mac.txbuff = buf
            self.DoMac(self, self.m_mac)
        else:
            self.Serial.write(buf)

    def mac_clear(self):
        if self.DoMac is not None:
            self.m_mac.mac_operate = RSMacLayer.RSMacOperate.Mac_Clear
            self.m_mac.mac_error = False
            self.DoMac(self, self.m_mac)
        else:
            self.Serial.discard_in_buffer()

    def on_serial_comm(self, data):
        if not self.AutoReceive:
            return

        self.m_rx.extend(data)
        # Processing logic for received data
        # This is a simplified version. You'll need to adjust it based on your actual data processing needs.
        rSFrame645Ex = RSFrame645Ex()
        bytes_read = rSFrame645Ex.pick_frame(self.m_rx)
        if bytes_read >= 0:
            if self.OnReceive is not None:
                self.OnReceive(self, rSFrame645Ex)
            # Adjust based on the frame length and processing logic
            self.m_rx = self.m_rx[bytes_read:]

    def stop(self):
        self.m_stop = True

    def send(self, tx_frame):
        self.mac_send(tx_frame.build_frame())

    def recv(self):
        self.m_stop = False
        rSFrame645Ex = RSFrame645Ex()
        # Placeholder for receive logic

    def comm(self, tx_frame):
        self.mac_clear()
        for _ in range(self.AttemptTimes):
            self.send(tx_frame)
            received_frame = self.recv()
            if received_frame is not None:
                return received_frame
        return None
