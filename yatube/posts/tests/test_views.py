from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from posts.models import Post, Group

User = get_user_model()


class PostPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.post = Post.objects.create(
            author=cls.user,
            text='тестовый текст',
        )
        cls.group = Group.objects.create(
            title='тестовое название',
            slug='test-slug',
            description='Тестовое описание',
        )

    def setUp(self):
        # Создаем авторизованный клиент
        self.user = User.objects.create_user(username='StasZatushevskii')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_uses_correct_template(self):
        """имя_html_шаблона: reverse(name)"""
        templates_pages_names = {
            'posts/index.html': reverse('posts:index'),
            'posts/group_list.html': reverse(
                'posts:group_posts', kwargs={'slug': 'test-slug'}),
            'posts/profile.html': reverse(
                'posts:profile', kwargs={'username': self.user.username}),
            'posts/post_detail.html': reverse(
                'posts:post_detail', kwargs={'post_id': self.post.id}),
            'posts/create_post.html': reverse('posts:post_create'),
        }

        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_post_list_page_show_correct_context(self):
        """Шаблон post_list сформирован с правильным контекстом."""
        post = self.cls.post
        response = (self.authorized_client.get(
            reverse('posts:group_posts', kwargs={'slug': 'test-slug'})))
        self.assertEqual(response.context.get(
            f'{post}').author, f'{self.user}')
        self.assertEqual(response.context.get('post').text, 'тестовый текст')
