import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = 'fsnanodegree2020.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'capstone'

# AuthError Exception

class AuthError(Exception):
    """
    AuthError Exception
    A standardized way to communicate auth failure modes
    """
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Auth Header

def get_token_auth_header():
    """
    Attempts to get the header from the request
    Raise an AuthError if no header is present
    It splits bearer and the token
    Raises an AuthError if the header is malformed

    Arguments:
        None

    Return:
        the token part of the header
    """

    auth_header = request.headers.get("Authorization")

    if not auth_header:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)

    token = auth_header.split(" ")

    if "bearer" != token[0].lower() or len(token) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be of type token bearer.'
        }, 401)

    if len(token) < 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found.'
        }, 401)

    return token[1]


def check_permissions(permission, payload):
    """
    It raises an AuthError if permissions are not included in the payload.
    It raises an AuthError if the requested permission string is not in the
    payload permissions array return true otherwise.
    
    Arguments:
        permission: string permission (i.e. 'post:drink')
        payload: decoded jwt payload

    Return:
        True
    """

    if "permissions" not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions not included in JWT.'
        }, 400)

    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'Unauthorized',
            'description': 'Permission not found.'
        }, 403)

    return True


def verify_decode_jwt(token):
    """
    Creates an Auth0 token with key id (kid).
    Verifies the token using Auth0 /.well-known/jwks.json.
    Decodes the payload from the token.
    Validates the claims.

    Arguments:
        token: a json web token (string)

    Return:
        the decodeded payload
    """

    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())

    # GET THE DATA IN THE HEADER
    unverified_header = jwt.get_unverified_header(token)

    # CHOOSE OUR KEY
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    # Finally, verify!!!
    if rsa_key:
        try:
            # USE THE KEY TO VALIDATE THE JWT
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)

        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)

    raise AuthError({
        'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
    }, 400)


def requires_auth(permission=''):
    """
    It uses the get_token_auth_header method to get the token.
    It uses the verify_decode_jwt method to decode the jwt.
    It uses the check_permissions method validate claims and check the requested permission.

    Arguments:
        permission: string permission (i.e. 'post:drink')
    
    Return:
        The decorator which passes the decoded payload to the decorated method
    """

    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator
