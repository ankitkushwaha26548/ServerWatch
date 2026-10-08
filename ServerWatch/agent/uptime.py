import time
import psutil


def get_uptime_seconds():
    boot_time = psutil.boot_time()
    current_time = time.time()
    return int(current_time - boot_time)

def format_uptime(seconds):
    days = seconds // 86400
    seconds = seconds % 86400
    hours = seconds // 3600
    seconds = seconds % 3600
    minutes = seconds // 60

    return f"{days} days, {hours} hours, {minutes} minutes"