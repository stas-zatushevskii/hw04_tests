from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import Group, Post
User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='тестовое название',
            slug='тестовый слаг',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='тестовая группа'
        )

    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        post = PostModelTest.post
        self.assertEqual(post.text, str(self.post.text[:15]))
        group = PostModelTest.group
        self.assertEqual(group.title, str(self.group.title))
