#
# (!) THIS MODULE IS AN OVERRIDE FOR: appleauth.apis
#
from appleauth.mixins import MultipleSerializerMixin
from appleauth.serializers import (
    AppleAuthCodeSerializer,
    AppleIDTokenSerializer,
    AppleTokenSerializer,
)
from appleauth.settings import apple_api_settings
from django.shortcuts import redirect
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny

from ..helpers import get_or_create_oauth_user
from ..oauth import oauth_authenticated_callback
from ..oauth.apple.services import AppleAuth


class AppleAuthViewset(MultipleSerializerMixin, viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    serializer_classes = {
        "authorize": AppleAuthCodeSerializer,
        "authorize_ios": AppleIDTokenSerializer,
        "token": AppleTokenSerializer,
    }

    @action(methods=["GET"], detail=False, url_path="redirect")
    def auth_url(self, request, *args, **kwargs):
        """
        url="oauth/apple/redirect/"
        """
        # Fetch Query Params
        extra_state = request.GET.get("state", None)
        redirect_url = request.GET.get("redirect_url", None)

        # Retrieve state and auth params
        apple_auth = AppleAuth()
        state = apple_auth.get_state(redirect_url, extra_state)
        auth_params = apple_auth.get_auth_params(state)

        authorization_url = (
            f"{apple_api_settings.APPLE_AUTHORIZATION_URL}?{auth_params}"
        )
        return redirect(authorization_url)

    @action(methods=["POST"], detail=False, url_path="callback")
    def authorize(self, request, *args, **kwargs):
        """
        url="oauth/apple/callback/"
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = serializer.validated_data["code"]
        apple_auth = AppleAuth(code=code)

        user_dict = apple_auth.do_auth()
        email = user_dict.get("email", None)

        user = get_or_create_oauth_user(email, service_name='Apple')
        return oauth_authenticated_callback(request, user)
