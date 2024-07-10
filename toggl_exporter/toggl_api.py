import base64
from datetime import datetime, timedelta

import requests


def load_toggl_config(config):
    return config["Toggl"]["api_token"]


def get_time_entries(api_token, start_date, end_date):
    base_url = "https://api.track.toggl.com/api/v9/me"
    api_token = f"{api_token}:api_token"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {base64.b64encode(api_token.encode()).decode()}",
    }
    url = f"{base_url}/time_entries?start_date={start_date}&end_date={end_date}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def process_time_entries(time_entries, timezone_offset):
    processed_entries = []
    for entry in time_entries[::-1]:
        # start_time = datetime.fromisoformat(entry["start"].replace("Z", "+00:00"))
        end_time = None
        if entry["stop"] is None:
            print(
                "WARNING: End time is not defined, which means the timer on the task is still going\nSkipping..."
            )
            continue
        else:
            end_time = datetime.fromisoformat(entry["stop"].replace("Z", "+00:00"))
        duration_hours = entry["duration"] / 3600  # Convert seconds to hours

        # Apply timezone offset
        offset = timedelta(hours=timezone_offset)
        # start_time_adjusted = start_time + offset
        end_time_adjusted = end_time + offset

        processed_entries.append(
            [
                end_time_adjusted.strftime("%d/%m/%Y"),
                end_time_adjusted.strftime("%H:%M"),
                round(duration_hours, 2),
                entry.get("description", ""),
                "",
            ]
        )
    return processed_entries
