from rest_framework.viewsets import ModelViewSet

from thing_pink.api import APICommonMixin

from .models import Post
from .serializers import PostSerializer


class PostViewSet(APICommonMixin, ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def filter_queryset(self, queryset):
        if self.request.user.is_anonymous():
            return queryset.public()
        return queryset

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = []
        return super(PostViewSet, self).get_permissions()
