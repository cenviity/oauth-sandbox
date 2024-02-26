# pyright: reportIncompatibleMethodOverride = false

# https://requests-oauthlib.readthedocs.io/en/latest/oauth1_workflow.html

import urllib.parse as urlparse

from dotenv import dotenv_values
from requests_cache import CacheMixin
from requests_oauthlib import OAuth1Session

config = dotenv_values(".env")

host_name = config.get("HOST_NAME")
base_url = f"http://{host_name}/gallery/api/"
assert base_url, "base_url has no value"
endpoint = "/admin/v1/workflows"

# Ensure there is no "/" at start of endpoint and one "/" at end of endpoint
url = urlparse.urljoin(base_url, endpoint.strip("/") + "/")

client_key = config.get("CLIENT_KEY")
client_secret = config.get("CLIENT_SECRET")


class CachedOAuth1Session(CacheMixin, OAuth1Session):
    pass


if __name__ == "__main__":
    print(url)

    session = CachedOAuth1Session(
        client_key=client_key,
        client_secret=client_secret,
        signature_type="auth_header",
        expire_after=3600,
    )
    # session.cache.clear()

    response = session.get(url)  # type: ignore
    print(response, response.reason)
    response.raise_for_status()

    data = response.json()
    print("Total workflows:", len(data))
