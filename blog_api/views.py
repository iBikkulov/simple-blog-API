from rest_framework import generics
from blog.models import Post
from .serializers import PostSerializer


class PostListView(generics.ListCreateAPIView):
    queryset = Post.postobjects.all()
    serializer_class = PostSerializer


class PostDetailView(generics.RetrieveDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer