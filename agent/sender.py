import os
import requests

from dotenv import load_dotenv


load_dotenv()


API_URL = os.getenv(
    "API_URL",
    "http://127.0.0.1:8000"
)

SERVER_ID = int(
    os.getenv("SERVER_ID", "1")
)


def send_metrics(data):

    payload = {
        "server_id": SERVER_ID,
        "cpu_usage": data["cpu_usage"],
        "memory_usage": data["memory_usage"],
        "disk_usage": data["disk_usage"],
        "network_sent_mb": data["network_sent_mb"],
        "network_received_mb": data["network_received_mb"],
        "uptime_seconds": data["uptime_seconds"]
    }

    response = requests.post(
        f"{API_URL}/metrics/",
        json=payload,
        timeout=5
    )

    response.raise_for_status()

    return response.json()