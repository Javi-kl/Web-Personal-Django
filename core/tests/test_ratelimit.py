from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


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
            response = self.client.post(self.url, data)
            # 200 (login fallido pero sin rate limit) o302 (redirección)
            self.assertIn(response.status_code, [200, 302])

    def test_6to_post_bloqueado(self):
        """La 6ª petición POST debe ser bloqueada (código 403)."""
        data = {"username": "testuser", "password": "testpass123"}

        # Hacer5 peticionespermitidas
        for i in range(5):
            self.client.post(self.url, data)

        # La 6ª debe ser bloqueada
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 403)


class RegisterViewRateLimitTest(TestCase):
    """
    Test: Rate limiting en RegisterView.
    Límite: 5 peticiones por hora por IP.
    """

    def setUp(self):
        self.url = reverse("core:register")

    def test_5_gets_permitidos(self):
        """Las primeras5 peticiones GET deben pasar (código 200)."""
        for i in range(5):
            response = self.client.get(self.url)
            self.assertEqual(response.status_code, 200)

    def test_6to_get_bloqueado(self):
        """La 6ª petición GET debe ser bloqueada (código 403)."""
        # Hacer5 peticiones permitidas
        for i in range(5):
            self.client.get(self.url)

        # La 6ª debe ser bloqueada
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)


class ContactFormViewRateLimitTest(TestCase):
    """
    Test: Rate limiting en ContactFormView.
    Límite: 2 peticiones POST por minuto por IP.
    """

    def setUp(self):
        self.url = reverse("core:contact")

    def test_2_posts_permitidos(self):
        """Las primeras 2 peticiones POST válidas deben pasar (código 302)."""
        data = {
            "email": "test@example.com",
            "comentario": "Este es un mensaje de prueba válido.",
        }

        for i in range(2):
            response = self.client.post(self.url, data)
            # 302 = redirección exitosa después de guardar
            self.assertEqual(response.status_code, 302)

    def test_3er_post_bloqueado(self):
        """La3ª petición POST debe ser bloqueada (código 403)."""
        data = {
            "email": "test@example.com",
            "comentario": "Este es un mensaje de prueba válido.",
        }

        # Hacer2 peticionespermitidas
        for i in range(2):
            self.client.post(self.url, data)

        # La 3ª debe ser bloqueada
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 403)
