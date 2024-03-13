import serial
from serial.tools import list_ports
import threading
import xml.etree.ElementTree as ET
import os

class RSSerial:
    def __init__(self):
        self.serial_port = serial.Serial()
        self.set_default()

    def set_default(self):
        self.serial_port.port = 'COM1'
        self.serial_port.baudrate = 9600
        self.serial_port.bytesize = serial.EIGHTBITS
        self.serial_port.parity = serial.PARITY_NONE
        self.serial_port.stopbits = serial.STOPBITS_ONE
        self.serial_port.rtscts = False
        self.serial_port.dsrdtr = False
        self.serial_port.xonxoff = False
        self.serial_port.timeout = None  # No timeout
        self.serial_port.writeTimeout = None  # No write timeout
        self.m_stop = False
        # Update port list if needed, here just assigning statically
        self.port_list = list(serial.tools.list_ports.comports())

    def open(self):
        if not self.serial_port.is_open:
            self.serial_port.open()

    def stop(self):
        self.m_stop = True

    def close(self):
        if self.serial_port.is_open:
            self.serial_port.close()

    def read(self, size=1):
        if self.serial_port.is_open:
            return self.serial_port.read(size)
        return None

    def write(self, data):
        if self.serial_port.is_open:
            self.serial_port.write(data)

    def save_config(self, file_name):
        config = ET.Element('SerialConfig')
        general = ET.SubElement(config, 'General')
        for attr in ['port', 'baudrate', 'bytesize', 'parity', 'stopbits', 'rtscts', 'dsrdtr', 'xonxoff']:
            value = getattr(self.serial_port, attr)
            ET.SubElement(general, attr).text = str(value)
        tree = ET.ElementTree(config)
        tree.write(file_name)

    def load_config(self, file_name):
        if os.path.exists(file_name):
            tree = ET.parse(file_name)
            config = tree.getroot().find('General')
            for attr in config:
                if hasattr(self.serial_port, attr.tag):
                    # Handle types accordingly, this example just shows the approach
                    setattr(self.serial_port, attr.tag, attr.text)

    def __str__(self):
        return f"{self.serial_port.port}: {self.serial_port.baudrate},{self.serial_port.parity},{self.serial_port.bytesize},{self.serial_port.stopbits}; Rts={self.serial_port.rtscts},Dtr={self.serial_port.dsrdtr};"

    # Implement WaitForData, ShowConfig, and ondata methods as required for your application

