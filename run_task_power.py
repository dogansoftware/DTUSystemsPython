import sys
from Common.CDTUSystem import CDTUSystem
from Common.CDTUMeter import CDTUMeter
from Common.CDTUSystemOption import CDTUSystemOption  # Make sure to import CDTUSystemOption


def task_power(system, flag):
    system.connect()
    # Example initialization, replace with actual logic to load meters
    meters = [CDTUMeter("Meter1"), CDTUMeter("Meter2")]

    for meter in meters:
        print(f"Processing {meter.MID}...")
        if system.power(meter, flag):
            power_status = "Power On" if meter.PowerStatus == 1 else "Power Off"
            print(f"{meter.MID}: {power_status}")
        else:
            print(f"{meter.MID}: Error - {meter.Error}")

    system.disconnect()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python run_task_power.py <flag>")
        sys.exit(1)

    flag = int(sys.argv[1])

    # Create and configure the options for CDTUSystem
    option = CDTUSystemOption()
    # Configure the option object as needed
    # Example configuration (adjust according to your needs)
    option.ReadMode = 'DTU_Remote_Read'  # or 'Local_Read'
    option.WaitTimeOut_Local = 5000
    option.WaitTimeOut_Remote = 10000
    option.RemoteHost = "example.com:12345"  # Example; adjust as needed

    # Now, create an instance of CDTUSystem with the configured option
    system = CDTUSystem(option)
    task_power(system, flag)
