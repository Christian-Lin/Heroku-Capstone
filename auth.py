import os
import json
from flask import request, _request_ctx_stack, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen

# AUTH0_DOMAIN = 'chris-fsnd.eu.auth0.com'
# API_AUDIENCE = 'Heroku'
AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN')
API_AUDIENCE = os.environ.get('API_AUDIENCE')
ALGORITHMS = ['RS256']

# AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Auth Header
def get_token_auth_header():
    # Fetches access token from auth header
    token = request.headers.get('Authorization', None)
    if not token:
        raise AuthError({
            'code': 'auth_header_not_found',
            'description': 'Authorization header not found'
        }, 401)

    # Split token ("Bearer" and token string)
    parts = token.split()

    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_auth_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)

    elif len(parts) == 1:
        raise AuthError({
            'code': 'invalid_auth_header',
            'description': 'Token not found.'
        }, 401)

    elif len(parts) > 2:
        raise AuthError({
            'code': 'invalid_auth_header',
            'description': 'Authorization header must have bearer token.'
        }, 401)

    # If all else passes, return token
    token = parts[1]
    return token


'''
Implement check_permissions(permission, payload) method
'''


def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_token',
            'description': 'Permissions not found'
        }, 400)

    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'Unauthorized',
            'description': 'Permission not allowed'
        }, 403)

    return True


'''
implement verify_decode_jwt(token) method
'''


def verify_decode_jwt(token):
    # Get public key from Auth0
    json_url = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(json_url.read())
    # Get header
    unverified_header = jwt.get_unverified_header(token)

    # Choose key
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise Autherror({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)
    # Loop to search for a match
    for key in jwks['keys']:
        rsa_key = {
            'kty': key['kty'],
            'kid': key['kid'],
            'use': key['use'],
            'n': key['n'],
            'e': key['e']
        }
        # Stop the loop
        break

    # Verify the signature (copied from the JWT documentation)
    if rsa_key:
        try:
            # Use key to validate the JWT
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
                'description': 'Incorrect claims. '
                'Please, check the audience and issuer.'
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


'''
implement @requires_auth(permission) decorator method
'''


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator
