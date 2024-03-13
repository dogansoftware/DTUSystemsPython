import xml.etree.ElementTree as ET
from typing import List
import os


class CDTUSystemOption:
    def __init__(self):
        self.host_list: List[str] = []
        self.read_mode = 'Local_Read'  # Assuming 'CDTUSystem_ReadMode.Local_Read'
        self.attempts = 2
        self.loops = 1
        self.default_schem = ""
        # self.serial_meter = RSSerial()  # Assuming RSSerial is previously converted and adapted
        self.wait_timeout_local = 5000
        self.remote_host = "39.108.253.153:6020"
        self.wait_timeout_remote = 10000
        # self.serial_config = str(self.serial_meter)

    def save_config(self, file_path):
        general_element = ET.Element("General")
        general_element.set("ReadMode", self.read_mode)
        general_element.set("Attempts", str(self.attempts))
        general_element.set("Loops", str(self.loops))
        general_element.set("DefautSchem", self.default_schem)
        general_element.set("WaitTimeOut_Local", str(self.wait_timeout_local))
        general_element.set("RemoteHost", self.remote_host)
        general_element.set("WaitTimeOut_Remote", str(self.wait_timeout_remote))

        option_tree = ET.ElementTree(general_element)
        option_tree.write(os.path.join(file_path, "Data", "Option.xml"))

        # Assume SerialMeter has a save_config method
        # self.serial_meter.save_config(os.path.join(file_path, "Data", "SerialConfig.xml"))

        with open(os.path.join(file_path, "Data", "Host.txt"), "w") as host_file:
            for host in self.host_list:
                host_file.write(f"{host}\n")

    def load_config(self, file_path):
        try:
            tree = ET.parse(os.path.join(file_path, "Data", "Option.xml"))
            root = tree.getroot()

            self.read_mode = root.get("ReadMode", self.read_mode)
            self.attempts = int(root.get("Attempts", self.attempts))
            self.loops = int(root.get("Loops", self.loops))
            self.default_schem = root.get("DefautSchem", self.default_schem)
            self.wait_timeout_local = int(root.get("WaitTimeOut_Local", self.wait_timeout_local))
            self.remote_host = root.get("RemoteHost", self.remote_host)
            self.wait_timeout_remote = int(root.get("WaitTimeOut_Remote", self.wait_timeout_remote))

            # Assume SerialMeter has a load_config method
            # self.serial_meter.load_config(os.path.join(file_path, "Data", "SerialConfig.xml"))

            host_path = os.path.join(file_path, "Data", "Host.txt")
            if os.path.exists(host_path):
                with open(host_path, "r") as host_file:
                    self.host_list = [line.strip() for line in host_file.readlines()]

        except Exception as e:
            print(f"Failed to load configuration: {e}")
