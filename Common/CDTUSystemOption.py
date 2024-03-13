import xml.etree.ElementTree as ET
from pathlib import Path

from Common.CDTUSystemReadMode import CDTUSystemReadMode
from Common.RSCommon.Serial.RSSerial import RSSerial


class CDTUSystemOption:
    def __init__(self):
        self.HostList = []
        self.ReadMode = CDTUSystemReadMode.Local_Read
        self.Attempts = 2
        self.Loops = 1
        self.DefaultSchem = ""
        self.SerialMeter = RSSerial() # Initialize your RSSerial instance as needed
        self.WaitTimeOut_Local = 5000
        self.RemoteHost = "39.108.253.153:6020"
        self.WaitTimeOut_Remote = 10000
        #self.SerialConfig = self.SerialMeter.toString() # Adjust based on RSSerial implementation

    def save_config(self, file_path):
        config_path = Path(file_path) / "Data"
        config_path.mkdir(parents=True, exist_ok=True)

        # SerialConfig.xml and Option.xml saving logic goes here
        # XML saving might depend on the structure of your RSSerial class

        # Saving HostList to Host.txt
        host_file_path = config_path / "Host.txt"
        with open(host_file_path, 'w') as file:
            file.write('\n'.join(self.HostList))

    def load_config(self, file_path):
        config_path = Path(file_path) / "Data"
        option_file_path = config_path / "Option.xml"
        host_file_path = config_path / "Host.txt"

        if option_file_path.exists():
            tree = ET.parse(option_file_path)
            root = tree.getroot()

            # Example of reading a single value:
            # self.ReadMode = root.find('General/ReadMode').text # Adjust based on actual XML structure

            # Similar logic for other properties

        if host_file_path.exists():
            with open(host_file_path, 'r') as file:
                self.HostList = [line.strip() for line in file.readlines()]

