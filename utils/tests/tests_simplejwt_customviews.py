from rest_framework.test import APITestCase
from rest_framework.response import Response
from utils.mixins.auth import UserMixin


class CustomTokenAbtainTests(APITestCase, UserMixin):
    token_obtain_url = '/api/token/'

    def setUp(self, *args, **kwargs) -> None:
        self.create_user()

        self.response = self.client.post(
            self.token_obtain_url, {
                'username': 'user',
                'password': 'password',
            },
        )

        return super().setUp(*args, **kwargs)

    def test_token_obtain_must_returns_just_an_access_token(self) -> None:
        self.assertIn(
            'access',
            self.response.content.decode('utf-8'),
        )

    def test_token_obtain_must_returns_an_cookie_http_only_with_token_refresh(self) -> None:  # noqa: E501
        self.assertIn(
            'token_refresh',
            self.response.cookies,
        )

    def test_token_obtain_must_returns_an_cookie_with_csrftoken(self) -> None:  # noqa: E501
        self.assertIn(
            'csrftoken',
            self.response.cookies,
        )

    def test_token_obtain_must_returns_status_code_401_if_invalid_credentials(self) -> None:  # noqa: E501
        response = self.client.post(
            self.token_obtain_url,
            {
                'username': 'jhon',
                'password': 'dhoe'
            },
        )

        self.assertEqual(
            response.status_code,
            401
        )


class CustomTokenRefreshTests(APITestCase, UserMixin):
    token_obtain_url = '/api/token/'
    token_refresh_url = '/api/token/refresh/'

    def create_refresh_token_by_cookie(self) -> Response:
        self.create_user()

        response = self.client.post(
            self.token_obtain_url, {
                'username': 'user',
                'password': 'password',
            },
        )

        return response

    def handle_response(self) -> Response:
        self.create_refresh_token_by_cookie()
        response = self.client.post(self.token_refresh_url)
        return response

    def test_token_refresh_view_must_returns_the_new_access_token(self) -> None:  # noqa: E501
        response = self.handle_response()
        self.assertIn(
            'access',
            response.content.decode('utf-8')
        )

    def test_token_refresh_view_must_not_returns_the_refresh_token(self) -> None:  # noqa: E501
        response = self.handle_response()
        self.assertNotIn(
            'refresh',
            response.content.decode('utf-8')
        )

    def test_token_refresh_view_must_returns_the_csrftoken(self) -> None:  # noqa: E501
        response = self.handle_response()
        self.assertIn(
            'csrftoken',
            response.cookies,
        )

    def test_token_refresh_view_must_returns_status_code_401_if_an_invalid_refresh_token(self) -> None:  # noqa: E501
        response = self.client.post(self.token_refresh_url)

        self.assertEqual(
            response.status_code,
            401,
        )
