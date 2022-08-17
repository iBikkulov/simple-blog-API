from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from blog.models import Category, Post


def get_password():
    return '12341234'


def create_user(username):
    password = get_password()
    return User.objects.create_user(username=username, password=password)


def create_category(name):
    return Category.objects.create(name=name)


def create_post(user):
    id = user.id
    return Post.objects.create(author_id=id, category_id=1, content='test',
        excerpt='test', slug='test', status='published', title='test')


class PostTests(APITestCase):

    def test_get_posts(self):
        """
        Ensure all users can view all posts.
        """
        url = reverse('blog_api:listcreate')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_post(self):
        """
        Ensure only authenticated users can create posts.
        """
        user = create_user(username='test_user')
        password = get_password()
        url = reverse('blog_api:listcreate')

        # Need to have at least one Category to be able
        # to create Post objects
        create_category(name='test_category')

        self.client.login(username=user.username, password=password)
        response = self.client.post(
            url, {
                'title': 'test',
                'author': 1,
                'excerpt': 'test',
                'content': 'test',
            }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_post(self):
        """
        Ensure only the author of the post can edit it.
        """
        user1 = create_user(username='test_user1')  # id = 1
        user2 = create_user(username='test_user2')  # id = 2
        password = get_password()
        url = reverse(('blog_api:detailcreate'), kwargs={'pk': 1})
        client = APIClient()

        # Need to have at least one Category to be able
        # to create Post objects
        create_category(name='test_category')

        # Create Post object owned by the user1
        create_post(user=user1)

        client.login(username=user2.username, password=password)
        response = client.put(
            url, {
                'id': 1, # post id
                'title': 'New',
                'author': 1, # author id
                'excerpt': 'New',
                'content': 'New',
                'status': 'published',
            }, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        client.login(username=user1.username, password=password)
        response = client.put(
            url, {
                'id': 1, # post id
                'title': 'New',
                'author': 1, # author id
                'excerpt': 'New',
                'content': 'New',
                'status': 'published',
            }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
