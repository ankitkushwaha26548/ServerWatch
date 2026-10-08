import time
import requests


def check_api(url: str):

    start_time = time.perf_counter()

    try:

        response = requests.get(
            url,
            timeout=5
        )

        end_time = time.perf_counter()

        response_time = (
            end_time - start_time
        ) * 1000

        if 200 <= response.status_code < 400:
            status = "healthy"

        else:
            status = "unhealthy"

        return {
            "status_code": response.status_code,
            "response_time": round(
                response_time,
                2
            ),
            "status": status,
            "error_message": None
        }

    except requests.RequestException as error:

        end_time = time.perf_counter()

        response_time = (
            end_time - start_time
        ) * 1000

        return {
            "status_code": None,
            "response_time": round(
                response_time,
                2
            ),
            "status": "down",
            "error_message": str(error)
        }