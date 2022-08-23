from rest_framework import serializers
from blog.models import Post


class PostSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.ReadOnlyField(source='author.user_name')
    url = serializers.HyperlinkedIdentityField(
        view_name='blog_api:detailcreate')

    class Meta:
        model = Post
        fields = [
            'id', 'url', 'title', 'author', 'excerpt',
            'slug', 'content', 'status',
        ]