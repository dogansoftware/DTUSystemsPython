from Common.RSCommon.DLT645.RSFrame645Ex import RSFrame645Ex
from Common.RSCommon.RSMacLayer import RSMacLayer
from Common.RSCommon.RSMacOperate import RSMacOperate

import time
from threading import Thread
from Common.RSCommon.RSTools import RSTools


class RSCommDLT645Ex:
    BUFFER_SIZE = 1024

    def __init__(self, socket, did):
        self.m_socket = socket
        self.m_did = did
        self.m_macError = ""
        self.m_mac = RSMacLayer()
        self.m_rx = bytearray()
        self.WaitTimeout = 5000
        self.AutoReceive = False
        self.AttemptTimes = 1
        self.HandleMessage = None  # Placeholder for event handler
        self.DoMac = None  # Placeholder for event handler
        self.OnReceive = None  # Placeholder for event handler
        self.m_macError = ""

    async def mac_send(self, buf):
        byte_list = bytearray()
        byte_list.append(126)
        byte_list.extend(RSTools.hex_str_to_byte_array(self.m_did.zfill(32)))
        length = len(buf)
        byte_list.append(length // 256)
        byte_list.append(length % 256)
        byte_list.extend(buf)
        byte_list.append(126)
        await self.m_socket.send(byte_list)

    async def mac_recv(self):
        source = await self.m_socket.wait_for_data()
        if source is None:
            print(f"Source was none")
            return None

        count = source[17] * 256 + source[18]
        array = source[19:19 + count]
        if count == 9 and array.decode("utf-8") == "No Online":
            self.m_macError = "DTU No Online"
            print(f"DTU No Online")
            return None
        elif count == 7 and array.decode("utf-8") == "No Busy":
            self.m_macError = "DTU Busy"
            print(f"DTU Busy")
            return None
        return array

    async def mac_clear(self):
      await   self.m_socket.clear_available()

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

    async def send(self, tx_frame: RSFrame645Ex):
        await self.mac_send(tx_frame.BuildFrame())

    # def recv(self):

    #   if not self.Serial.serial_port.is_open:
    #        print("Serial port is not open.")
    #       return []
    #    self.m_stop = False
    #   received_frames = []
    #  buffer = bytearray()
    # start_time = time.time()

    # while (time.time() - start_time) < (self.WaitTimeout / 1000) and not self.m_stop:
    #   if self.Serial.in_waiting > 0:
    #        data = self.Serial.read(self.Serial.in_waiting)
    #       buffer.extend(data)

    #       while True:
    # Attempt to parse a frame from the buffer
    #            success, frame = RSFrame645Ex.try_parse(buffer)
    #            if success:
    #               received_frames.append(frame)
    # Assuming frame also provides its total length, so we know how much to slice off the buffer
    #               frame_len = frame.GetFrameLen()
    #               buffer = buffer[frame_len:]  # Remove processed frame from buffer
    #            else:
    #              break  # Exit the loop if no valid frame could be parsed from the current buffer

    # return received_frames

    async def comm(self, tx_frame: RSFrame645Ex):
        await self.mac_clear()
        await self.send(tx_frame)
        received_frames = await self.mac_recv()
        if received_frames is None:
            received_frames = []  # Ensure it's always an iterable
        return received_frames
