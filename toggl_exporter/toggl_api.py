from datetime import datetime

import requests


def load_toggl_config(config):
    return config["Toggl"]["api_token"], config["Toggl"]["workspace_id"]


def get_time_entries(api_token, start_date, end_date):
    base_url = "https://api.track.toggl.com/api/v8"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {api_token}",
    }
    url = f"{base_url}/time_entries?start_date={start_date}&end_date={end_date}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def process_time_entries(time_entries):
    processed_entries = []
    for entry in time_entries:
        start_time = datetime.fromisoformat(entry["start"].replace("Z", "+00:00"))
        end_time = datetime.fromisoformat(entry["stop"].replace("Z", "+00:00"))
        duration_hours = entry["duration"] / 3600  # Convert seconds to hours

        processed_entries.append(
            [
                end_time.strftime("%d/%m/%Y"),
                end_time.strftime("%H:%M"),
                round(duration_hours, 2),
                entry.get("description", ""),
                "",
            ]
        )
    return processed_entries
