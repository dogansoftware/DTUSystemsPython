from Common.RSCommon.DLT645.RSFrame645Ex import RSFrame645Ex
from Common.RSCommon.RSMacLayer import RSMacLayer
from Common.RSCommon.RSMacOperate import RSMacOperate
from Common.RSCommon.Serial.RSSerial import RSSerial
import time
from threading import Thread

class RSCommDLT645Ex:
    BUFFER_SIZE = 1024

    def __init__(self):
        self.m_stop = False
        self.m_auto = False
        self.m_mac = RSMacLayer()
        self.m_rx = bytearray()
        self.Serial = RSSerial()  # Adjust with your Serial configuration
        self.WaitTimeout = 5000
        self.AutoReceive = False
        self.AttemptTimes = 1
        self.HandleMessage = None  # Placeholder for event handler
        self.DoMac = None  # Placeholder for event handler
        self.OnReceive = None  # Placeholder for event handler
        self.m_macError = ""

    def mac_recv(self):
        if self.Serial.serial_port.is_open and self.Serial.in_waiting > 0:
            return self.Serial.read(self.Serial.in_waiting)
        return bytearray()

    def mac_send(self, buf):
        self.Serial.write(buf)

    def mac_clear(self):
        self.Serial.discard_in_buffer()

    def do_mac(self, mac: RSMacLayer):
        if mac.MacOperate == RSMacOperate.Mac_Send:
            self.mac_send(mac.TxBuf)
        elif mac.MacOperate == RSMacOperate.Mac_Receive:
            mac.RxBuf = self.mac_recv()
            if self.m_macError:
                mac.MacError = True
        elif mac.MacOperate == RSMacOperate.Mac_Clear:
            self.mac_clear()

    def on_serial_comm(self):
        # Simulate SerialDataReceivedEventHandler
        while self.AutoReceive and not self.m_stop:
            data = self.mac_recv()
            if data:
                self.m_rx.extend(data)
                # Assuming RSFrame645Ex can parse frames from m_rx
                frame = RSFrame645Ex.try_parse(self.m_rx)
                if frame:
                    if self.OnReceive:
                        self.OnReceive(self, frame)
                    # Remove processed data from m_rx
                    self.m_rx = self.m_rx[len(frame):]

            time.sleep(0.1)  # Prevent tight loop

    def start_auto_receive(self):
        self.AutoReceive = True
        thread = Thread(target=self.on_serial_comm)
        thread.start()

    def stop(self):
        self.m_stop = True

    def send(self, tx_frame: RSFrame645Ex):
        self.mac_send(tx_frame.BuildFrame())

    def recv(self):
        if not self.Serial.serial_port.is_open:
            print("Serial port is not open.")
            return []
        self.m_stop = False
        received_frames = []
        buffer = bytearray()
        start_time = time.time()

        while (time.time() - start_time) < (self.WaitTimeout / 1000) and not self.m_stop:
            if self.Serial.in_waiting > 0:
                data = self.Serial.read(self.Serial.in_waiting)
                buffer.extend(data)

                while True:
                    # Attempt to parse a frame from the buffer
                    success, frame = RSFrame645Ex.try_parse(buffer)
                    if success:
                        received_frames.append(frame)
                        # Assuming frame also provides its total length, so we know how much to slice off the buffer
                        frame_len = frame.GetFrameLen()
                        buffer = buffer[frame_len:]  # Remove processed frame from buffer
                    else:
                        break  # Exit the loop if no valid frame could be parsed from the current buffer

        return received_frames

    def comm(self, tx_frame: RSFrame645Ex):
        self.mac_clear()
        self.send(tx_frame)
        received_frame = self.recv()
        return received_frame