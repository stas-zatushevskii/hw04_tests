import shutil
import tempfile

from posts.models import Post, Group
from django.conf import settings
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from django.contrib.auth import get_user_model
User = get_user_model()

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.post = Post.objects.create(
            author=cls.user,
            text='тестовая группа'
        )
        cls.group = Group.objects.create(title='Тестовая', slug='test')

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        # Создаем неавторизованный клиент
        self.guest_client = Client()
        self.author_client = Client()
        self.user = User.objects.create_user(username='StasZatushevskii')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.author_client.force_login(self.user)

    def test_create_post(self):
        post_count = Post.objects.count()

        form_data = {
            'group': self.group.id,
            'text': 'Тестовый текст',
        }
        response = self.guest_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse('posts:profile',
                             kwargs={'username': self.user.username}))
        self.assertEqual(Post.objects.count(), post_count + 1)
        self.assertTrue(    
            Post.objects.filter(
                text='Тестовый текст',
                group='Тестовая группа'
            ).exists())

    def post_edit_(self):
        post = self.cls.post
        form_data_edit = {
            'group': 'Тестовая группа',
            'text': 'Тестовый отредоктированный текст',
        }

        response = self.author_client.post(
            reverse('posts:post_edit'),
            data=form_data_edit,
            follow=True
        )
        self.assertRedirects(response, reverse(
            'profile', kwargs={'username': 'test_user'})
        )
        self.assertNotEqual(post, response)
