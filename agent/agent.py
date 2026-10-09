from utils import bytes_to_mb

from metrics import (
    get_cpu_usage,
    get_memory_usage,
    get_disk_usage,
    get_network_usage
)

from system_info import (
    get_hostname,
    get_operating_system,
    get_os_version,
    get_cpu_information
)

from uptime import (
    get_uptime_seconds,
    format_uptime
)


def collect_metrics():

    network = get_network_usage()

    uptime_seconds = get_uptime_seconds()

    cpu_info = get_cpu_information()

    return {
        "hostname": get_hostname(),
        "operating_system": get_operating_system(),
        "os_version": get_os_version(),

        "cpu_usage": get_cpu_usage(),

        "memory_usage": get_memory_usage(),

        "disk_usage": get_disk_usage(),

        "network_sent_mb": bytes_to_mb(
            network["bytes_sent"]
        ),

        "network_received_mb": bytes_to_mb(
            network["bytes_received"]
        ),

        "physical_cores": cpu_info["physical_cores"],

        "logical_cores": cpu_info["logical_cores"],

        "uptime_seconds": uptime_seconds,

        "uptime": format_uptime(uptime_seconds)
    }


if __name__ == "__main__":

    data = collect_metrics()

    print("\n================================")
    print("       ServerWatch Agent")
    print("================================")

    for key, value in data.items():
        print(f"{key}: {value}")

    print("================================\n")
