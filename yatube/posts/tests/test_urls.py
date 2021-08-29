from django.test import TestCase
from django.test import Client
from ..models import Post, Group
from django.contrib.auth import get_user_model

User = get_user_model()

class StaticURLTests(TestCase):
    def setUp(self):
        # Устанавливаем данные для тестирования
        # Создаём экземпляр клиента. Он неавторизован.
        self.guest_client = Client()

    def test_homepage(self):
        # Создаем экземпляр клиента
        act = self.guest_client
        # Делаем запрос к главной странице и проверяем статус
        response = act.get('/')
        # Утверждаем, что для прохождения теста код должен быть равен 200
        self.assertEqual(response.status_code, 200)

    def test_author(self):
        act = self.guest_client
        response = act.get('/about/author/')
        self.assertEqual(response.status_code, 200)

    def test_tech(self):
        act = self.guest_client
        response = act.get('/about/tech/')
        self.assertEqual(response.status_code, 200)


class PostsUrlsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username = 'auth')
        cls.post = Post.objects.create(
            author=cls.user,
            text='тестовая группа',
        )
        cls.group = Group.objects.create(
            title='тестовое название',
            slug='test-slug',
            description='Тестовое описание',
        )
        
    def setUp(self):
        # неавторизированный клиент
        self.guest_client = Client()
        # пользователь 
        self.user = User.objects.create(username = 'HasNoName')
        # авторизированный клиент 
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_urls_uses_correct_template(self):
        # Шаблон : адрес
        templates_url_names = {
            'posts/index.html' : '/',
            'posts/post_detail.html' : f'/posts/{self.post.id}/',
            'posts/create_post.html' : '/create/',
            'posts/profile.html' : f'/profile/{self.user.username}/',
            'posts/group_list.html' : '/group/test-slug/'
        }

        for template, adress in templates_url_names.items():
            with self.subTest(adress=adress):
                response = self.authorized_client.get(adress)
                self.assertTemplateUsed(response, template) 