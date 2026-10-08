import psutil
import platform 
import socket


def get_hostname():
    return socket.gethostname()

def get_operating_system():
    return platform.system()

def get_os_version():
    return platform.version()

def get_cpu_information():
    return {
        "physical_cores": psutil.cpu_count(logical=False),
        "logical_cores": psutil.cpu_count(logical=True),
    }