# Toggl to Google Sheets Exporter

This project allows you to export your Toggl time entries to a Google Sheets spreadsheet, with support for timezone adjustments.

## Table of Contents
1. [Features](#features)
2. [Prerequisites](#prerequisites)
3. [Setup](#setup)
4. [Usage](#usage)
5. [Configuration](#configuration)
6. [Troubleshooting](#troubleshooting)
7. [Contributing](#contributing)
8. [License](#license)

## Features

- Fetch time entries from Toggl Track API
- Export time entries to Google Sheets
- Timezone adjustment support
- Automatic appending of new entries without duplication
- Configurable date range for exporting

## Prerequisites

- Python 3.7 or higher
- Poetry dependency manager
- A Toggl account with API access
- A Google account with access to Google Sheets
- Google Cloud project with Sheets API enabled

## Setup

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/toggl-to-sheets-exporter.git
   cd toggl-to-sheets-exporter
   ```

2. Install required dependencies:
   ```
   poetry install
   ```

3. Set up Google Sheets API credentials:
   - Go to the [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one
   - Enable the Google Sheets API
   - Create credentials (OAuth client ID)
   - Download the client configuration and save it as `credentials.json` in the root directory of the project

4. Configure your Toggl API token and Google Sheet ID in `config.ini`

## Usage

Run the script in the root directory of the project with:

```
poetry run toggle-exporter
```

## Configuration

Edit the `config.json` file to set:

- `toggl_api_token`: Your Toggl API token
- `spreadsheet_id`: The ID of your Google Sheet
- `timezone_offset`: The number of hours to adjust the times (e.g., 2 for +2 hours, -4 for -4 hours)
- `range`: The range of the spreadsheet

## Troubleshooting

- If you encounter permission errors, ensure that:
  - Your Google account has edit access to the specified spreadsheet
  - The necessary API scopes are enabled in your Google Cloud project
  - Your `credentials.json` file is up to date

- For Toggl API issues, verify your API token and check Toggl's API status

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.
