"""GitHub integration installation authentication.

https://developer.github.com/early-access/integrations/authentication/
"""

import datetime

import jwt
import requests

__all__ = ['create_jwt', 'get_installation_token']


def get_installation_token(installation_id, integration_jwt):
    """Create a GitHub token for an integration installation.

    Parameters
    ----------
    installation_id : `int`
        Installation ID. This is available in the URL of the integration's
        **installation** ID.
    integration_jwt : `bytes`
        The integration's JSON Web Token (JWT). This is created by
        `create_jwt`.

    Returns
    -------
    token_obj : `dict`
        GitHub token object. Includes the fields:

        - ``token``: the token string itself.
        - ``expires_at``: date time string when the token expires.
        - ``on_behalf_of``: user that has authenticated.

    Example
    -------
    The typical workflow for authenticating to an integration installation is:

    .. code-block:: python

       from dochubadapter.github import auth
       jwt = auth.create_jwt(integration_id, private_key_path)
       token_obj = auth.get_installation_token(installation_id, jwt)
       print(token_obj['token'])
    """
    # https://developer.github.com/early-access/integrations/authentication/#as-an-installation
    # curl -i -X POST \
    #     -H "Authorization: Bearer $JWT" \
    #     -H "Accept: application/vnd.github.machine-man-preview+json" \
    #     https://api.github.com/installations/:installation_id/access_tokens

    url = ('https://api.github.com/installations/'
           '{installation_id:d}/access_tokens'.format(
               installation_id=installation_id))

    headers = {
        'Authorization': 'Bearer {0}'.format(integration_jwt.decode('utf-8')),
        'Accept': 'application/vnd.github.machine-man-preview+json'
    }

    resp = requests.post(url, headers=headers)
    resp.raise_for_status()
    return resp.json()


def create_jwt(integration_id, private_key_path):
    """Create a JSON Web Token for authenticate a GitHub Integration or
    installation.

    Parameters
    ----------
    integration_id : `int`
        Integration ID. This is available from the GitHub integration's
        homepage.
    private_key_path : `str`
        Path to the integration's private key (a ``.pem`` file).

    Returns
    -------
    jwt : `bytes`
        JSON Web Token that is good for 9 minutes.

    Notes
    -----
    https://developer.github.com/early-access/integrations/authentication/
    """
    integration_id = int(integration_id)

    with open(private_key_path, 'rb') as f:
        cert_str = f.read()

    time_delta = datetime.timedelta(minutes=9)
    now = datetime.datetime.now()
    expiration_time = datetime.datetime.now() + time_delta
    payload = {
        # Issued at time
        'iat': int(now.timestamp()),
        # JWT expiration time (10 minute maximum)
        'exp': int(expiration_time.timestamp()),
        # Integration's GitHub identifier
        'iss': integration_id
    }

    return jwt.encode(payload, cert_str, algorithm='RS256')
