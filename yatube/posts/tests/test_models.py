from django.test import TestCase
from ..models import Group, Post
from django.contrib.auth import get_user_model
User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        '''тестовая запись'''
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
        text = self.post.text
        self.assertEqual(post.text, str(text))
        group = PostModelTest.group
        title = self.group.title
        self.assertEqual(group.title, str(title))
