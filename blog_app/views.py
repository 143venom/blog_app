from rest_framework.generics import GenericAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from django.contrib.auth import authenticate
from .models import *
from .serializers import *
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from .permissions import CustomModelPermission, IsOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


@api_view(['POST'])
def register(request):
    password = request.data.get('password')
    hash_password = make_password(password)
    request.data['password'] = hash_password
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'data': 'User Created!'})
    else:
        return Response({'error': serializer.errors})


@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(username=email, password=password)
    if user is None:
        return Response('User not found in Database')
    else:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
    
class UserListCreateView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile_objects = self.get_queryset()
        serializer = UserSerializer(profile_objects, many=True)
        return Response({'data': serializer.data})

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data})
        return Response({'error':serializer.errors})

class UserDetailView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get(self, request, pk):
        user_profile_object = User.objects.get(id=pk)
        serializer = self.get_serializer(user_profile_object)
        return Response({'data': serializer.data})

    def put(self, request, pk):
        user_profile_object = User.objects.get(id=pk)
        self.check_object_permissions(request, user_profile_object)
        serializer = self.get_serializer(user_profile_object, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': "Profile Updated Successfull"})
        return Response({'error':serializer.errors})

    def delete(self, request, pk):
        user_profile_object = User.objects.get(id=pk)
        self.check_object_permissions(request, user_profile_object)
        user_profile_object.delete()
        return Response({'message': 'Data deleted successfull'})

class ProfileListCreateView(GenericAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['full_name', 'address']
    search_fields = ['full_name', 'address']

    def get(self, request):
        profile_objects = self.filter_queryset(self.get_queryset())
        serializer = ProfileSerializer(profile_objects, many=True)
        return Response({'data': serializer.data})

    def post(self, request):
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data})
        return Response({'error':serializer.errors})

class ProfileDetailView(GenericAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get(self, request, pk):
        user_profile_object = Profile.objects.get(id=pk)
        serializer = self.get_serializer(user_profile_object)
        return Response({'data': serializer.data})

    def put(self, request, pk):
        user_profile_object = Profile.objects.get(id=pk)
        self.check_object_permissions(request, user_profile_object)
        serializer = self.get_serializer(user_profile_object, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': "Profile Updated Successfull"})
        return Response({'error':serializer.errors})

    def delete(self, request, pk):
        user_profile_object = Profile.objects.get(id=pk)
        self.check_object_permissions(request, user_profile_object)
        user_profile_object.delete()
        return Response({'message': 'Data deleted successfull'})
    
class PostListCreateView(GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['title', 'content']
    search_fields = ['title', 'content']

    def get(self, request):
        profile_objects = self.filter_queryset(self.get_queryset())
        serializer = PostSerializer(profile_objects, many=True)
        return Response({'data': serializer.data})

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': "post created successfully"})
        return Response({'error':serializer.errors})

class PostDetailView(GenericAPIView):
    queryset = Profile.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get(self, request, pk):
        user_profile_object = Post.objects.get(id=pk)
        serializer = self.get_serializer(user_profile_object)
        return Response({'data': serializer.data})

    def put(self, request, pk):
        user_profile_object = Post.objects.get(id=pk)
        self.check_object_permissions(request, user_profile_object)
        serializer = self.get_serializer(user_profile_object, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': "Post Updated Successfull"})
        return Response({'error':serializer.errors})

    def delete(self, request, pk):
        user_profile_object = Post.objects.get(id=pk)
        self.check_object_permissions(request, user_profile_object)
        user_profile_object.delete()
        return Response({'message': 'Data deleted successfull'})


class CommentListCreateView(GenericAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['post', 'text']
    search_fields = ['post', 'text']

    def get(self, request):
        profile_objects = self.filter_queryset(self.get_queryset())
        serializer = CommentSerializer(profile_objects, many=True)
        return Response({'data': serializer.data})

    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data})
        return Response({'error':serializer.errors})

class CommentDetailView(GenericAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get(self, request, pk):
        user_profile_object = Comment.objects.get(id=pk)
        serializer = self.get_serializer(user_profile_object)
        return Response({'data': serializer.data})

    def put(self, request, pk):
        user_profile_object = Comment.objects.get(id=pk)
        self.check_object_permissions(request, user_profile_object)
        serializer = self.get_serializer(user_profile_object, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': "comment Updated Successfully!"})
        return Response({'error':serializer.errors})

    def delete(self, request, pk):
        user_profile_object = Comment.objects.get(id=pk)
        self.check_object_permissions(request, user_profile_object)
        user_profile_object.delete()
        return Response({'message': 'Data deleted successfull'})
    
class LikeListCreateView(GenericAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile_objects = self.get_queryset()
        serializer = LikeSerializer(profile_objects, many=True)
        return Response({'data': serializer.data})

    def post(self, request):
        serializer = LikeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data})
        return Response({'error':serializer.errors})

class LikeDetailView(GenericAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get(self, request, pk):
        user_profile_object = Like.objects.get(id=pk)
        serializer = self.get_serializer(user_profile_object)
        return Response({'data': serializer.data})

    def put(self, request, pk):
        user_profile_object = Like.objects.get(id=pk)
        self.check_object_permissions(request, user_profile_object)
        serializer = self.get_serializer(user_profile_object, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': "Profile Updated Successfull"})
        return Response({'error':serializer.errors})

    def delete(self, request, pk):
        user_profile_object = Like.objects.get(id=pk)
        self.check_object_permissions(request, user_profile_object)
        user_profile_object.delete()
        return Response({'message': 'Data deleted successfull'})

class ActivityFeedView(GenericAPIView):
    serializer_class = serializers.Serializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        activity_type = self.request.query_params.get('type')

        if activity_type == 'comments':
            return CommentSerializer
        elif activity_type == 'likes':
            return LikeSerializer
        else:
            return PostSerializer

    def data_activity(self):
        user = self.request.user
        friends = Friendship.objects.filter(user=user).values_list('friend', flat=True)
        posts = Post.objects.filter(user__in=friends).order_by('-created_at')[:5]
        # posts = Post.objects.filter().order_by('-created_at')[:3]
        comments = Comment.objects.filter(user__in=friends).order_by('-created_at')[:5]
        likes = Like.objects.filter(user__in=friends).order_by('-id')[:5]
        merged_activity = sorted(list(posts) + list(comments) + list(likes), key=lambda instance: getattr(instance, 'created_at', instance.id), reverse=True)
        return merged_activity

    def get(self, request, *args, **kwargs):
        queryset = self.data_activity()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)
        return Response({'data':serializer.data})
        
        