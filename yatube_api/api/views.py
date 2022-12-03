from api.permissions import IsAuthorOrReadOnly
from api.serializers import (CommentSerializer, FollowSerializer,
                             GroupSerializer, PostSerializer)
from django.shortcuts import get_object_or_404
from posts.models import Comment, Follow, Group, Post
from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated


class CreateRetrieveListViewSet(mixins.CreateModelMixin,
                                mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                viewsets.GenericViewSet):
    """
    Кастомный вьюсет для обработки только
    GET- и POST-запросов.
    """
    pass


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Обрабатывем все типы запросов к группам."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    pagination_class = None


class PostViewSet(viewsets.ModelViewSet):
    """Обрабатывем все типы запросов к постам."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly, ]
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        """При создании поста, автором назначается
        авторизованный пользователь"""
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """Обрабатывем все типы запросов к комментам."""
    permission_classes = [IsAuthorOrReadOnly, ]
    serializer_class = CommentSerializer
    pagination_class = None

    def get_queryset(self):
        """Получаем список комментариев к определенному посту."""
        post_id = self.kwargs.get("post_id")
        new_queryset = Comment.objects.filter(post=post_id)
        return new_queryset

    def perform_create(self, serializer):
        """Создаём коментарий к определенному посту."""
        post_id = self.kwargs.get("post_id")
        post = get_object_or_404(Post, id=post_id)
        serializer.save(author=self.request.user, post=post)


class FollowViewSet(CreateRetrieveListViewSet):
    """Обрабатывем GET- и POST-запросы к подпискам."""
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated, ]
    pagination_class = None
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^following__username',)

    def get_queryset(self):
        """Получаем список подписчиков пользователя."""
        new_queryset = Follow.objects.filter(user=self.request.user)
        return new_queryset

    def perform_create(self, serializer):
        """Создаём подписку пользователя, который сделал запрос
        на пользователя переданного в теле запроса."""
        serializer.save(user=self.request.user)
