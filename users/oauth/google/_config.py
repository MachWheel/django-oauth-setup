from random import SystemRandom

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from ._models import GoogleLoginServiceCredentials


def get_service_credentials() -> GoogleLoginServiceCredentials:
    client_id = settings.GOOGLE_OAUTH2_CLIENT_ID
    client_secret = settings.GOOGLE_OAUTH2_CLIENT_SECRET
    project_id = settings.GOOGLE_OAUTH2_PROJECT_ID

    if not client_id:
        raise ImproperlyConfigured("GOOGLE_OAUTH2_CLIENT_ID missing in env.")

    if not client_secret:
        raise ImproperlyConfigured("GOOGLE_OAUTH2_CLIENT_SECRET missing in env.")

    if not project_id:
        raise ImproperlyConfigured("GOOGLE_OAUTH2_PROJECT_ID missing in env.")

    return GoogleLoginServiceCredentials(client_id, client_secret, project_id)


def generate_state_session_token(length=30) -> str:
    # Official SDK implementation
    unicode_ascii_charset = (
        'abcdefghijklmnopqrstuvwxyz'
        'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        '0123456789'
    )
    rand = SystemRandom()
    state = "".join(
        rand.choice(unicode_ascii_charset) for _ in range(length)
    )
    return state
