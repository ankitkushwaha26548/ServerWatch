import os
import requests

from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")
AGENT_TOKEN = os.getenv("AGENT_TOKEN")

SERVER_ID = int(os.getenv("SERVER_ID", "1"))


def send_metrics(data):
    if not AGENT_TOKEN:
        raise ValueError(
            "AGENT_TOKEN is missing. Check your agent .env file."
        )

    payload = {
        "server_id": SERVER_ID,
        "cpu_usage": data["cpu_usage"],
        "memory_usage": data["memory_usage"],
        "disk_usage": data["disk_usage"],
        "network_sent_mb": data["network_sent_mb"],
        "network_received_mb": data["network_received_mb"],
        "uptime_seconds": data["uptime_seconds"],
    }

    response = requests.post(
        f"{API_URL}/metrics/",
        json=payload,
        headers={"X-Agent-Token": AGENT_TOKEN},
        timeout=5,
    )

    response.raise_for_status()
    return response.json()