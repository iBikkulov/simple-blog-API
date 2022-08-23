from rest_framework import generics
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly, IsAuthenticated
)
from blog.models import Post
from .serializers import PostSerializer
from .permissions import PostUserWritePermission


class PostListView(generics.ListCreateAPIView):
    queryset = Post.postobjects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly & PostUserWritePermission
    ]
