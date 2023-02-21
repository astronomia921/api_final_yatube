from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters, permissions, viewsets
from rest_framework.pagination import LimitOffsetPagination

from posts.models import Group, Post

from .permissions import OwnerOrReadOnly, ReadOnly
from .serializers import (
    CommentSerializer,
    FollowSerializer,
    GroupSerializer,
    PostSerializer)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (OwnerOrReadOnly, )
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,
                       filters.OrderingFilter)
    ordering_fields = ('author', 'username')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_permissions(self):
        if self.action == 'retrieve':
            return (ReadOnly(),)
        return super().get_permissions()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (OwnerOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def get_post(self):
        post = get_object_or_404(Post, id=self.kwargs.get("post_id"))
        return post

    def get_queryset(self):
        post = self.get_post()
        new_queryset = post.comments.select_related('post')
        return new_queryset

    def perform_create(self, serializer):
        post = self.get_post()
        serializer.save(author=self.request.user, post=post)

    def get_permissions(self):
        if self.action == 'retrieve':
            return (ReadOnly(),)
        return super().get_permissions()


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = GroupSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        post_id = self.kwargs.get("post_id")
        new_queryset = Group.objects.filter(posts=post_id)
        return new_queryset

    def perform_create(self, serializer):
        group = get_object_or_404(Group, id=self.kwargs.get('group_id'))
        serializer.save(author=self.request.user.is_staff, group=group)


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        return self.request.user.follower.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
