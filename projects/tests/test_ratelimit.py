from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from projects.models import ProjectModel


class ProjectCommentRateLimitTest(TestCase):
    """
    Test: Rate limiting en ProjectDetailView (creación de comentarios).
    Límite: 5 peticiones POST por minuto por IP.
    """

    def setUp(self):
        # Crear proyecto y usuario para los tests
        self.project = ProjectModel.objects.create(
            title="Proyecto de prueba", description="Descripción de prueba"
        )
        self.user = User.objects.create_user(
            username="comentador", password="testpass123"
        )
        self.url = reverse("projects:project_detail", kwargs={"pk": self.project.pk})

    def test_5_comments_permitidos(self):
        """
        Las primeras5 peticiones POST con comentario válido deben pasar.
        """
        self.client.login(username="comentador", password="testpass123")
        data = {"content": "Este es un comentario de prueba válido."}

        for i in range(5):
            response = self.client.post(self.url, data)
            # 302 = redirección exitosa después de crear comentario
            self.assertEqual(response.status_code, 302)

    def test_6to_comment_bloqueado(self):
        """
        La6ª petición POST debe ser bloqueada (código 403).
        """
        self.client.login(username="comentador", password="testpass123")
        data = {"content": "Este es un comentario de prueba válido."}

        # Hacer5 peticiones permitidas
        for i in range(5):
            self.client.post(self.url, data)

        # La6ª debe ser bloqueada
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 403)

    def test_get_no_afectado_por_ratelimit(self):
        """
        Laspeticiones GET (ver proyecto) no deben verse afectadas.
        """
        self.client.login(username="comentador", password="testpass123")
        data = {"content": "Este es un comentario de prueba válido."}

        # Hacer5 comentarios (agotar rate limit POST)
        for i in range(5):
            self.client.post(self.url, data)

        # POST siguiente debe ser bloqueado
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 403)

        # Pero GET debe seguir funcionando
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
