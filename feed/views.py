from rest_framework.viewsets import ModelViewSet

from thing_pink.api import APICommonMixin

from .models import Post
from .serializers import PostSerializer


class PostViewSet(APICommonMixin, ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_fields = ('search',)

    def filter_queryset(self, queryset):
        # this allows the user to only change his own posts
        if self.request.method == 'GET':
            queryset = queryset.feed_for_user(self.request.user)
        elif self.request.method in ['DELETE', 'PATCH', 'PUT']:
            queryset = queryset.from_user(self.request.user)

        # search parameters
        search_param = self.request.query_params.get('search')
        if search_param:
            queryset = queryset.filter(partials__text__icontains=search_param)

        return queryset

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = []
        return super(PostViewSet, self).get_permissions()
