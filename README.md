# oauth-sandbox

Playing around with OAuth 1.0 and 2.0 authentication

## Getting started

1. Install Poetry: https://python-poetry.org/docs/#installation
2. Install dependencies:

    ```shell
    poetry install
    ```
3. Rename `.env.template` to `.env` and add in config values:

    | Configuration   | Example                                         |
    | --------------- | ----------------------------------------------- |
    | `HOST_NAME`     | `alteryx.<hostname>.com` (without `http(s)://`) |
    | `CLIENT_KEY`    | API key                                         |
    | `CLIENT_SECRET` | API secret                                      |

4. Run the scripts with Poetry (replace `requests_oauthlib_oauth1.py` below with any other script).

    **Using Poetry's virtual environment:**

    ```shell
    poetry shell
    python requests_oauthlib_oauth1.py
    ```

    **Outside of Poetry's virtual environment:**

    ```shell
    poetry run python requests_oauthlib_oauth1.py
    ```
