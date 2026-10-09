import os
import psutil


def get_cpu_usage():
    return psutil.cpu_percent(interval=1)


def get_memory_usage():
    memory = psutil.virtual_memory()
    return memory.percent


def get_disk_usage():
    if os.name == "nt":
        disk = psutil.disk_usage("C:\\")
    else:
        disk = psutil.disk_usage("/")

    return disk.percent


def get_network_usage():
    network = psutil.net_io_counters()

    return {
        "bytes_sent": network.bytes_sent,
        "bytes_received": network.bytes_recv
    }
