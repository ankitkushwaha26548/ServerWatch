import requests

from sender import API_URL


def send_log(
    server_id,
    level,
    message,
    source="agent"
):

    payload = {
        "server_id": server_id,
        "level": level,
        "message": message,
        "source": source
    }

    try:

        response = requests.post(
            f"{API_URL}/logs/",
            json=payload,
            timeout=5
        )

        response.raise_for_status()

        return response.json()

    except requests.RequestException as error:

        print(
            "Failed to send log:",
            error
        )

        return None