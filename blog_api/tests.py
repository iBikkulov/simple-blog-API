from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from users.models import NewUser
from blog.models import Category, Post


def get_password():
    return '12341234'


def create_user(user_name, email):
    password = get_password()
    return NewUser.objects.create_user(user_name=user_name,
                                       email=email,
                                       first_name='first_name',
                                       password=password)


def create_category(name):
    return Category.objects.create(name=name)


def create_post(user):
    id = user.id
    return Post.objects.create(author_id=id, category_id=1, content='test',
                               excerpt='test', slug='test', status='published',
                               title='test')


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
        user = create_user(user_name='test_user',
                           email='test_user@example.com')
        password = get_password()
        auth_url = reverse('token_obtain_pair')
        create_post_url = reverse('blog_api:listcreate')

        # Need to have at least one Category to be able
        # to create Post objects
        create_category(name='test_category')

        # Use JWT Authentication
        response = self.client.post(auth_url, {
            'email': user.email,
            'password': password
        })
        self.assertTrue('access' in response.data)
        access_token = response.data.get('access')

        response = self.client.post(create_post_url, {
            'title': 'test',
            'slug': 'test',
            'content': 'test',
        }, format='json', HTTP_AUTHORIZATION=f'JWT dummy_token')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.post(create_post_url, {
            'title': 'test',
            'slug': 'test',
            'content': 'test',
        }, format='json', HTTP_AUTHORIZATION=f'JWT {access_token}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_post(self):
        """
        Ensure only the author of the post can edit it.
        """
        user1 = create_user(user_name='test_user1',
                            email='test_user1@example.com')  # id = 1
        user2 = create_user(user_name='test_user2',
                            email='test_user2@example.com')  # id = 2
        password = get_password()
        auth_url = reverse('token_obtain_pair')
        detail_url = reverse(('blog_api:detailcreate'), kwargs={'pk': 1})
        client = APIClient()

        # Need to have at least one Category to be able
        # to create Post objects
        create_category(name='test_category')

        # Create Post object owned by the user1
        create_post(user=user1)

        # Use JWT Authentication for user1
        response = self.client.post(auth_url, {
            'email': user1.email,
            'password': password
        })
        self.assertTrue('access' in response.data)
        access_token_user1 = response.data.get('access')

        response = self.client.put(detail_url, {
            'title': 'New1',
            'slug': 'New1',
            'content': 'New1',
        }, format='json', HTTP_AUTHORIZATION=f'JWT {access_token_user1}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Use JWT Authentication for user2
        response = self.client.post(auth_url, {
            'email': user2.email,
            'password': password
        })
        self.assertTrue('access' in response.data)
        access_token_user2 = response.data.get('access')

        response = self.client.put(detail_url, {
            'title': 'New2',
            'slug': 'New1',
            'content': 'New2',
        }, format='json', HTTP_AUTHORIZATION=f'JWT {access_token_user2}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
