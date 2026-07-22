from unittest.mock import patch

from django.test import TestCase
from django.http import HttpResponse
from django.core.cache import cache
from django.urls import reverse
from typing import cast


class UserLoginViewRateLimitTest(TestCase):
    """
    Test: Rate limiting en UserLoginView.
    Límite: 5 peticiones POST por minuto por IP.
    """

    def setUp(self):
        cache.clear()
        self.url = reverse("core:login")

    def tearDown(self):
        cache.clear()

    @patch("django_ratelimit.core.time.time", return_value=1_700_000_000)
    def test_login_blocks_sixth_attempt(self, mocked_time):
        credentials = {
            "username": "usuario-inexistente",
            "password": "incorrecta",
        }
        client_ip = "198.51.100.10"

        for _ in range(5):
            response = cast(
                HttpResponse,
                self.client.post(
                    self.url,
                    credentials,
                    REMOTE_ADDR=client_ip,
                ),
            )
            self.assertEqual(
                response.status_code,
                200,
            )
        blocked_response = cast(
            HttpResponse,
            self.client.post(
                self.url,
                credentials,
                REMOTE_ADDR=client_ip,
            ),
        )
        self.assertEqual(
            blocked_response.status_code,
            403,
        )
