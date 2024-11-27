from django.contrib.auth import logout
from django.shortcuts import redirect
from rest_framework import permissions
from rest_framework.views import APIView

from ..oauth.google import GoogleLoginService


class GoogleLoginRedirectApi(APIView):
    """
    url="oauth/google/redirect/"
    name="api_oauth_google_redirect"
    """
    authentication_classes = ()
    permission_classes = (permissions.AllowAny,)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)

        authorization_url, request.session["google_oauth2_state"] = (
            GoogleLoginService().get_authorization_url()
        )

        return redirect(authorization_url)
