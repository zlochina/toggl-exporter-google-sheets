import configparser
from datetime import datetime, timedelta

from .google_sheets_api import export_to_google_sheets, load_google_config
from .toggl_api import (get_time_entries, load_toggl_config,
                        process_time_entries)


def load_config():
    config = configparser.ConfigParser()
    config.read("config.ini")
    return config


def load_general_config(config):
    return config["General"]


def main():
    config = load_config()
    api_token = load_toggl_config(config)
    spreadsheet_id, range_name = load_google_config(config)
    timezone_offset = load_general_config(config).getint("timezone_offset")

    end_date = datetime.now()
    start_date = end_date - timedelta(days=1)

    start_date_str = start_date.strftime("%Y-%m-%dT%H:%M:%SZ")
    end_date_str = end_date.strftime("%Y-%m-%dT%H:%M:%SZ")

    try:
        time_entries = get_time_entries(api_token, start_date_str, end_date_str)
        processed_entries = process_time_entries(time_entries, timezone_offset)

        export_to_google_sheets(processed_entries, spreadsheet_id, range_name)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
