from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.models import User


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user: User, timestap):
        return (
         str(user.pk) + str(timestap) + str(user.is_active)  # noqa E501
        )


account_activation_token = AccountActivationTokenGenerator()
