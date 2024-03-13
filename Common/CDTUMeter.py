class CDTUMeter:
    def __init__(self):
        self.m_mid = "1".zfill(12)[:12]  # Python's zfill is similar to PadLeft
        self.m_did = "0".zfill(24)[:24]
        self.DTU = None  # Assuming DTU is another class you will define
        self.UserID = 0
        self.ProtocolType = 0
        self.SchemID = 0
        self.LastValue = ""
        self.LastReadDateTime = ""
        self.OLDMID = self.m_mid
        self.Comment = ""
        self.DataList = []  # Assuming CDTUMeterData is another class you will define
        self.ProducttKey = ""
        self.DeviceName = ""
        self.DeviceSecret = ""
        self.PowerStatus = 0
        self.ReadResult = 0
        self.Error = ""

    @property
    def MID(self):
        return self.m_mid

    @MID.setter
    def MID(self, value):
        self.m_mid = value.zfill(12)[:12]

    @property
    def DID(self):
        return self.m_did

    @DID.setter
    def DID(self, value):
        value = value.strip()
        self.m_did = value.zfill(24)[:24]

    def __str__(self):
        return self.m_mid
