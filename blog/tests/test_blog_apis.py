from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.test import TestCase

from blog.models import Post
from blog.serializers import PostDetailSerializer

POSTS_URL = reverse('blog:post-list')


def detail_url(post_id):
    return reverse('blog:post-detail', args=[post_id])


def create_user(**params):
    """Create and return a new user"""
    return get_user_model().objects.create(**params)


class PostTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email="user@example.com", password="test123")
        self.client.force_authenticate(user=self.user)

    def test_publish_post_by_author(self):
        """Test publishing a post by the author"""
        payload = {
            'title': 'Test Post',
            'content': 'This is a test post'
        }
        res = self.client.post(POSTS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        post = Post.objects.get(id=res.data['id'])
        self.assertEqual(post.title, payload['title'])
        self.assertEqual(post.content, payload['content'])
        self.assertEqual(post.author, self.user)

    def test_list_published_posts_with_author(self):
        """Test listing published posts with data about author"""
        post1 = Post.objects.create(title='Post 1', content='Content 1', author=self.user)
        post2 = Post.objects.create(title='Post 2', content='Content 2', author=self.user)

        res = self.client.get(POSTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        posts = Post.objects.all()
        serializer = PostDetailSerializer(posts, many=True)
        self.assertEqual(res.data, serializer.data)

    def test_update_post_by_author(self):
        """Test updating a post by the author"""
        post = Post.objects.create(title='Old Title', content='Old Content', author=self.user)
        new_payload = {'title': 'New Title', 'content': 'New Content'}

        url = detail_url(post.id)
        res = self.client.patch(url, new_payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        post.refresh_from_db()
        self.assertEqual(post.title, new_payload['title'])
        self.assertEqual(post.content, new_payload['content'])

    def test_delete_post_by_author(self):
        """Test deleting a post by the author"""
        post = Post.objects.create(title='To Be Deleted', content='Delete Me', author=self.user)

        url = detail_url(post.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(id=post.id).exists())

    def test_delete_post_by_non_author(self):
        """Test deleting a post by a user who is not the author"""
        user2 = create_user(email="user2@example.com", password="test1234")
        post = Post.objects.create(title='To Be Deleted', author=user2)

        url = detail_url(post.id)

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Post.objects.filter(id=post.id).exists())

    def test_update_post_no_permission(self):
        """Test updating a post without permission"""
        user2 = create_user(email="user2@example.com", password="test456")
        post = Post.objects.create(title='Post by Author', content='Update Me', author=self.user)
        payload = {'title': 'Updated Title', 'content': 'Updated Content'}

        self.client.force_authenticate(user=user2)
        url = detail_url(post.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        post.refresh_from_db()
        self.assertNotEqual(post.title, payload['title'])
        self.assertNotEqual(post.content, payload['content'])
