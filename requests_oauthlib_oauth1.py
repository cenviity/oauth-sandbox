# https://requests-oauthlib.readthedocs.io/en/latest/oauth1_workflow.html

import urllib.parse as urlparse

from dotenv import dotenv_values
from requests_oauthlib import OAuth1Session

config = dotenv_values(".env")

base_url = config.get("API_URL_OAUTH1")
assert base_url, "base_url has no value"
endpoint = "/admin/v1/workflows"

# Ensure there is no "/" at start of endpoint and one "/" at end of endpoint
url = urlparse.urljoin(base_url, endpoint.strip("/") + "/")

client_key = config.get("CLIENT_KEY")
client_secret = config.get("CLIENT_SECRET")


if __name__ == "__main__":
    print(url)

    session = OAuth1Session(
        client_key=client_key,
        client_secret=client_secret,
        signature_type="auth_header",
    )

    response = session.get(url)
    print(response, response.reason)
    response.raise_for_status()

    data = response.json()
    print("Total workflows:", len(data))
