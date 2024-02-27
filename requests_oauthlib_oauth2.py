# pyright: reportIncompatibleMethodOverride = false

# https://requests-oauthlib.readthedocs.io/en/latest/oauth2_workflow.html

import urllib.parse as urlparse

from dotenv import dotenv_values
from oauthlib.oauth2 import BackendApplicationClient
from requests.exceptions import ConnectTimeout
from requests_cache import CacheMixin
from requests_oauthlib import OAuth2Session

config = dotenv_values(".env")

host_name = config.get("HOST_NAME")
base_url = f"https://{host_name}/webapi/"
assert base_url, "base_url has no value"

token_endpoint = "/oauth2/token"
endpoint = "/v3/workflows"

# Ensure there is no "/" at start or end of token endpoint
token_url = urlparse.urljoin(base_url, token_endpoint.strip("/"))
# Ensure there is no "/" at start of endpoint and one "/" at end of API endpoint
endpoint_url = urlparse.urljoin(base_url, endpoint.strip("/") + "/")

client_key = config.get("CLIENT_KEY")
client_secret = config.get("CLIENT_SECRET")


class CachedOAuth2Session(CacheMixin, OAuth2Session):
    pass


def use_http(url: str) -> str:
    protocol = "https://"
    return "http://" + url.lstrip(protocol)


if __name__ == "__main__":
    client = BackendApplicationClient(client_id=client_key)
    # Don't cache token request
    session = OAuth2Session(
        client=client,
        expire_after=3600,
    )

    try:
        print("Token endpoint:", token_url)
        token = session.fetch_token(  # type: ignore
            token_url=token_url,
            client_secret=client_secret,
            timeout=5,
        )
    # Try HTTP if HTTPS times out
    except ConnectTimeout:
        token_url = use_http(token_url)
        print("Token endpoint:", token_url)

        import os

        # Override for using plain HTTP rather than HTTPS
        # https://oauthlib.readthedocs.io/en/latest/oauth2/security.html
        print("Resorting to insecure HTTP instead of HTTPS!")
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
        token = session.fetch_token(  # type: ignore
            token_url=token_url,
            client_secret=client_secret,
        )
        # Unset environment variable once we are done overriding
        del os.environ["OAUTHLIB_INSECURE_TRANSPORT"]
        endpoint_url = use_http(endpoint_url)

    print(token)

    # Do cache actual requests after getting token
    session = CachedOAuth2Session(
        client=client,
        expire_after=3600,
    )

    response = session.get(endpoint_url)  # type: ignore
    print(response, response.reason)
    response.raise_for_status()

    data = response.json()
    print("Total workflows:", len(data))
