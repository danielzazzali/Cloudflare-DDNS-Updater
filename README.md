# Cloudflare DDNS Updater

This script automatically updates DNS records in Cloudflare to match your device's current IP address. It uses the Cloudflare API to manage DNS records and is configured with environment variables for security.

## Requirements

- Python 3.10
- Cloudflare account with API access

## Installation

1. **Install dependencies**:

    Install the `python-dotenv` package using `pip`:

    ```bash
    pip install python-dotenv
    ```

## Configuration

1. **Clone the repository**:

    ```bash
    git clone https://github.com/danielzazzali/Cloudflare-DDNS-Updater
    cd Cloudflare-DDNS-Updater
    ```

2. **Create a `.env` file**:

    Copy the `.env.example` file to a new file named `.env`:

    ```bash
    cp .env.example .env
    ```

3. **Edit the `.env` file**:

    Open the `.env` file and configure the variables according to your Cloudflare details and preferences:

    - `AUTH_TOKEN`: Your authentication token for the Cloudflare API.
    - `API_HOST`: The Cloudflare API host (typically `api.cloudflare.com`).
    - `API_PATH`: The base path of the Cloudflare API (typically `/client/v4/`).
    - `ZONE_ID`: The ID of the Cloudflare zone where your DNS records are.
    - `PROXIED`: Whether the DNS records should be proxied by Cloudflare (true or false).
    - `TTL`: The time-to-live for the DNS records.
    - `LOG_FILE_PATH`: The path to the log file where the script will write its output.


## Usage

1. **Run the script**:

    ```bash
    python3 main.py
    ```

    The script will do the following:

    - Verify your authentication token with Cloudflare.
    - Obtain your current IP address.
    - Retrieve the DNS records for the specified zone.
    - Update all DNS records in Cloudflare to match your current IP address.
    - Print the update results for each DNS record.

## Notes

- Make sure to protect your `.env` file and keep it secure, as it contains sensitive information.
- If you encounter any issues or errors, check the API documentation for Cloudflare for troubleshooting tips.
