from django.contrib.auth import logout
from rest_framework import serializers, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from ..oauth import oauth_authenticated_callback
from ..oauth.google import GoogleLoginService, GoogleUserData
from ..helpers import get_or_create_oauth_user


class GoogleLoginCallbackApi(APIView):
    """
    url="oauth/google/callback/"
    name="api_oauth_google_callback"
    """
    authentication_classes = ()
    permission_classes = (permissions.AllowAny,)

    class InputSerializer(serializers.Serializer):
        code = serializers.CharField(required=False)
        error = serializers.CharField(required=False)
        state = serializers.CharField(required=False)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)

        input_serializer = self.InputSerializer(data=request.GET)
        input_serializer.is_valid(raise_exception=True)
        valid_data = input_serializer.validated_data

        error = valid_data.get("error")
        if error is not None:
            return _ERROR_400(error)

        code = valid_data.get("code")
        state = valid_data.get("state")
        if None in (code, state):
            return _MISSING_CODE_STATE_400()

        session_state = request.session.get("google_oauth2_state")
        if session_state is None:
            return _CSRF_FAILED_400()
        del request.session["google_oauth2_state"]
        if state != session_state:
            return _CSRF_FAILED_400()

        login_service = GoogleLoginService()
        access_tokens = login_service.get_tokens(code=code)
        user_data = GoogleUserData(access_tokens).__dict__
        user = get_or_create_oauth_user(**user_data, service_name='Google')
        return oauth_authenticated_callback(request, user)


def _ERROR_400(error: str):
    return Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)


def _CSRF_FAILED_400():
    return Response({"error": "CSRF check failed."}, status=status.HTTP_400_BAD_REQUEST)


def _MISSING_CODE_STATE_400():
    Response({"error": "Code and state are required."}, status=status.HTTP_400_BAD_REQUEST)
