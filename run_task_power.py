import sys
from Common.CDTUSystem import CDTUSystem
from Common.CDTUMeter import CDTUMeter
from Common.CDTUSystemOption import CDTUSystemOption
from Common.CDTUSystemReadMode import CDTUSystemReadMode


def task_power(system, meter_id="600000763434", flag=1):
    system.connect()
    # Initialize meter with the provided ID
    meter = CDTUMeter(meter_id)

    print(f"Processing {meter.MID}...")
    if system.power(meter, flag):
        power_status = "Power On" if meter.PowerStatus == 1 else "Power Off"
        print(f"{meter.MID}: {power_status}")
    else:
        print(f"{meter.MID}: Error - {meter.Error}")

    system.disconnect()

if __name__ == "__main__":
    # Default values for flag and meter_id
    flag = 1  # Default flag value if not provided
    meter_id = "600000763434"  # Default Meter ID if not provided
    remote_host = "39.108.253.153:6020"

    # Check command-line arguments and override default values if provided
    if len(sys.argv) > 1:
        flag = int(sys.argv[1])
    if len(sys.argv) > 2:
        meter_id = sys.argv[2]
    if len(sys.argv) > 3:
        meter_id = sys.argv[3]

    # Create and configure the options for CDTUSystem
    option = CDTUSystemOption()
    option.ReadMode = CDTUSystemReadMode.DTU_Remote_Read  # or 'Local_Read'
    option.WaitTimeOut_Local = 5000
    option.WaitTimeOut_Remote = 10000
    option.RemoteHost = remote_host  # Example; adjust as needed

    # Create an instance of CDTUSystem with the configured option
    system = CDTUSystem(option)
    task_power(system, meter_id, flag)
