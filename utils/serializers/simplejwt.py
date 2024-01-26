from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from typing import override, Dict, Any


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    @override
    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        super().validate(attrs)
        refresh = self.token_class(attrs["refresh"])
        data = {
            "access": str(refresh.access_token),
        }

        return data
