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

    def test_login_blocks_sixth_attempt(self):
        credentials = {
            "username": "usuario-inexistente",
            "password": "incorrecta",
        }
        client_ip = "198.51.100.10"

        for attempt in range(5):
            with self.subTest(attempt=attempt + 1):
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
