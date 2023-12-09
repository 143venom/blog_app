from rest_framework import serializers
from .models import *


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['full_name', 'address', 'bio']

class UserSerializer(serializers.ModelSerializer):
    # profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['email', 'password']

class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['title', 'content', 'created_at']

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('id','post', 'text', 'created_at')

class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Like
        fields = ('id', 'user', 'content_type','created_at', 'object_id', 'content_object')