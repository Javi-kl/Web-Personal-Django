from django.contrib.auth.models import User
from django.test import TestCase
from django.http import HttpResponse
from django.urls import reverse
from typing import cast


class UserLoginViewRateLimitTest(TestCase):
    """
    Test: Rate limiting en UserLoginView.
    Límite: 5 peticiones POST por minuto por IP.
    """

    def setUp(self):
        self.url = reverse("core:login")
        # Usuario existente para probar login
        User.objects.create_user(username="testuser", password="testpass123")

    def test_5_posts_permitidos(self):
        """Las primeras 5 peticiones POST deben pasar (código 200)."""
        data = {"username": "testuser", "password": "testpass123"}

        for i in range(5):
            response = cast(HttpResponse, self.client.post(self.url, data))
            # 200 (login fallido pero sin rate limit) o302 (redirección)
            self.assertIn(response.status_code, [200, 302])

    def test_6to_post_bloqueado(self):
        """La 6ª petición POST debe ser bloqueada (código 403)."""
        data = {"username": "testuser", "password": "testpass123"}

        # Hacer5 peticionespermitidas
        for i in range(5):
            self.client.post(self.url, data)

        # La 6ª debe ser bloqueada
        response = cast(HttpResponse, self.client.post(self.url, data))
        self.assertEqual(response.status_code, 403)
