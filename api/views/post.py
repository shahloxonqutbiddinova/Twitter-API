from rest_framework.decorators import permission_classes
from rest_framework.viewsets import ViewSet, ModelViewSet
from api.serializers import PostSerializer, MediaSerializer
from api.models import Post, Media, Comment
from rest_framework.permissions import IsAuthenticated, AllowAny
from api.permissions import IsAuthenticatedAndAuthor, IsAuthenticatedAndDone
from drf_spectacular.utils import extend_schema


@extend_schema(tags=["Post"])
class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_permissions(self):
        if self.action != "list":
            permission_classes = [AllowAny, ]
        elif self.action == "create":
            permission_classes = [IsAuthenticatedAndDone]
        else:
            permission_classes = [IsAuthenticatedAndAuthor, ]

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

