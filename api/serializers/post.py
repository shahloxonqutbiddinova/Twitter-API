from rest_framework import serializers
from api.models import Media, Post, Comment
from .user import UserSerializer


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['content', ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['user'] = UserSerializer(instance.user).data
        data['liked_users'] = UserSerializer(instance.liked_users, many = True).data
        data['viewed_users'] = UserSerializer(instance.viewed_users, many=True).data
        return data

class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = "__all__"
