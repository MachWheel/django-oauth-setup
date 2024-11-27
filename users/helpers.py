import random
import string

from django.contrib.auth.models import User
from django.utils import timezone

from .models import OauthUser

_short_id_chars = string.ascii_lowercase + string.digits + string.ascii_uppercase
_digit_chars = string.digits


def random_str(length=11) -> str:
    return ''.join(random.choices(_short_id_chars, k=length))


def get_or_create_oauth_user(email, first_name='Cliente', last_name='', service_name='unknown') -> User:
    try:
        oauth_user = OauthUser.objects.get(email=email)

    except OauthUser.DoesNotExist:
        oauth_user = OauthUser.objects.create(
            first_name=first_name.title(),
            last_name=last_name.title() if last_name else service_name.title(),
            email=email,
            service_name=service_name.title()
        )

    try:
        user = User.objects.get(email=email)

    except User.DoesNotExist:
        user = User.objects.create_user(
            email=email,
            password=random_str(),
            first_name=oauth_user.first_name,
            last_name=oauth_user.last_name,
            email_confirmed=True,
        )

    if not user.email_confirmed:  # confirm the previous existing user with oauth
        user.email_confirmed = True
        user.date_confirmed = timezone.now()
        user.save()

    return user
