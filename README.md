# Toggl Exporter

This script exports Toggl Track time entries from the last 24 hours to a Google Spreadsheet.

## Setup

1. Install Poetry: https://python-poetry.org/docs/#installation
2. Clone this repository
3. Run `poetry install` to install dependencies
4. Set up a Google Cloud Project and enable the Google Sheets API
5. Download the client configuration file and save it as `credentials.json` in the project directory
6. Copy `config.ini.sample` to `config.ini` and fill in your Toggl API token, workspace ID, and Google Spreadsheet ID

## Usage

Run the script using Poetry:
```sh
poetry run toggl-exporter
```

This will update your specified Google Spreadsheet with your time entries from the last 24 hours.
