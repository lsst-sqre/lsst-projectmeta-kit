"""GitHub integration installation authentication.

https://developer.github.com/early-access/integrations/authentication/
"""

import datetime

import jwt

__all__ = ['create_jwt']


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
