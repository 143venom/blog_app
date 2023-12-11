from rest_framework import serializers
from .models import *


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['full_name', 'address', 'bio']

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['id','email','profile']

class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Post
        fields = ['id','title','content','created_at','user']

class CommentSerializer(serializers.ModelSerializer):
    post = PostSerializer()

    class Meta:
        model = Comment
        fields = ('id','post', 'text', 'created_at')

class LikeSerializer(serializers.ModelSerializer):
    post = PostSerializer()
    class Meta:
        model = Like
        fields = ('object_id','id','content_type','post')
# class LikeSerializer(serializers.ModelSerializer):
#     # user = UserSerializer()
#     # post = PostSerializer()
#     class Meta:
#         model = Like
#         fields = ('object_id','id','user_id','post_id','content_type')