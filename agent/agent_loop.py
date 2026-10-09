import os
import time

from dotenv import load_dotenv

from agent import collect_metrics
from sender import SERVER_ID, send_metrics
from logger import send_log


load_dotenv()

SERVER_ID = int(
    os.getenv("SERVER_ID", "1")
)


INTERVAL = int(
    os.getenv("MONITOR_INTERVAL", "5")
)

cycle_count = 0

while True:

    try:

        data = collect_metrics()

        if data["cpu_usage"] > 80:
            send_log(
                SERVER_ID,
                "WARNING",
                f"High CPU usage: {data['cpu_usage']}%"
            )

        if data["memory_usage"] > 80:
            send_log(
                SERVER_ID,
                "WARNING",
                f"High memory usage: {data['memory_usage']}%"
            )

        if data["disk_usage"] > 80:
            send_log(
                SERVER_ID,
                "WARNING",
                f"High disk usage: {data['disk_usage']}%"
            )   

            if data["disk_usage"] > 90:
                send_log(
                    SERVER_ID,
                    "WARNING",
                    f"High disk usage: {data['disk_usage']}%"
                    )
                
        result = send_metrics(data)

        print("\n================================")
        print("ServerWatch Agent")
        print("================================")

        print(f"CPU: {data['cpu_usage']}%")
        print(f"RAM: {data['memory_usage']}%")
        print(f"Disk: {data['disk_usage']}%")

        print(
            f"Metrics sent successfully."
            f" Metric ID: {result['id']}"
        )

        print("================================\n")

    except Exception as error:

        print("Failed to send metrics.")
        print("Error:", error)

        cycle_count += 1

        if cycle_count %12 == 0:
            send_log(
                SERVER_ID,
                "INFO",
                "Metrics sent successfully"
            )

    time.sleep(INTERVAL)