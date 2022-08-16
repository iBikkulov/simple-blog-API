from django.test import TestCase
from django.contrib.auth.models import User
from .models import Post, Category


class Test_Create_Post(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        test_category = Category.objects.create(name="django")
        test_user = User.objects.create_user(username='test_user',
            password='12341234')
        test_post = Post.objects.create(author_id=1, category_id=1,
            title='Post title', content='Post content',
            excerpt='Post excerpt', slug='post-title', status='published')

    def test_blog_content(self):
        post = Post.postobjects.get(id=1)
        cat = Category.objects.get(id=1)
        author = f'{post.author}'
        excerpt = f'{post.excerpt}'
        title = f'{post.title}'
        content = f'{post.content}'
        status = f'{post.status}'

        self.assertEqual(author, 'test_user')
        self.assertEqual(title, 'Post title')
        self.assertEqual(content, 'Post content')
        self.assertEqual(status, 'published')
        self.assertEqual(str(post), 'Post title')   # test __str__ method
        self.assertEqual(str(cat), 'django')   # test __str__ method
