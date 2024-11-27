from urllib.parse import urlencode

from django.contrib.auth import user_logged_in
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

from ..models import AuthToken


class CustomSchemeRedirect(HttpResponseRedirect):
    allowed_schemes = ['myapp']  # TODO: replace with your schema


def oauth_authenticated_callback(request, user: User):
    token_instance, token = AuthToken.objects.create(user)
    user_logged_in.send(sender=user.__class__, request=request, user=user)
    query_params = urlencode({
        "token": token,
        "expiry": token_instance.expiry
    })

    # TODO: replace with your schema AND domain:
    redirect_url = f"myapp://login.mydomain.com.br/callback?{query_params}"

    return CustomSchemeRedirect(redirect_url)
