from django.test import TestCase
from django.contrib.auth import get_user_model
from blog.models import Post


class PostModelTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            password='testpass123',
            name='Test User'
        )

    def test_post_created_at_auto_now_add(self):
        """Test created_at field is auto-generated"""
        post = Post.objects.create(
            title='Auto Add ',
            content='This post is a post',
            author=self.user
        )
        self.assertIsNotNone(post.created_at)

    def test_post_updated_at_auto_now(self):
        """Test updated_at field """
        post = Post.objects.create(
            title='Auto update Post',
            content='This post should have its updated',
            author=self.user
        )
        old_updated_at = post.updated_at
        post.content = 'Updated content'
        post.save()
        self.assertNotEqual(old_updated_at, post.updated_at)
