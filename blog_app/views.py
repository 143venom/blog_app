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
from .permissions import IsOwnerOrReadOnly, CustomModelPermission
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

# user register
@api_view(['POST'])
def register(request):
    password = request.data.get('password')
    hash_password = make_password(password)
    request.data['password'] = hash_password
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Registration successfully'})
    else:
        return Response({'error': serializer.errors})
    

# user login
@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(username=email, password=password)
    if user is None:
        return Response({'message':'User not found in Database'})
    else:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
    
    
# user list and posting user
class UserListCreateView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['username', 'email']
    search_fields = ['username', 'email']

    def get(self, request):
        profile_objects = self.filter_queryset(self.get_queryset())
        serializer = UserSerializer(profile_objects, many=True)
        return Response({'data': serializer.data})

    # def post(self, request):
    #     serializer = UserSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response({'data': serializer.data})
    #     return Response({'error':serializer.errors})
    
# getting user detail 
class UserDetailView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        user_profile_object = User.objects.get(id=pk)
        serializer = self.get_serializer(user_profile_object)
        return Response({'data': serializer.data})

    def put(self, request, pk):
        user_profile_object = User.objects.get(id=pk)
        # checking isownerorreadonly to perform update operation
        self.check_object_permissions(request, user_profile_object)
        serializer = self.get_serializer(user_profile_object, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': "Profile Updated Successfull"})
        return Response({'error':serializer.errors})

    def delete(self, request, pk):
        user_profile_object = User.objects.get(id=pk)
        # checking isownerorreadonly to perform delete operation
        self.check_object_permissions(request, user_profile_object)
        user_profile_object.delete()
        return Response({'message': 'Data deleted successfull'})
    
    
# getting profile list and posting user profile
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
    

# getting Detail profile list and posting user profile
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
        # checking isownerorreadonly to perform update operation
        self.check_object_permissions(request, user_profile_object)
        serializer = self.get_serializer(user_profile_object, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': "Profile Updated Successfull"})
        return Response({'error':serializer.errors})

    def delete(self, request, pk):
        user_profile_object = Profile.objects.get(id=pk)
        # checking isownerorreadonly to perform delete operation
        self.check_object_permissions(request, user_profile_object)
        user_profile_object.delete()
        return Response({'message': 'Data deleted successfull'})
    
    
#creating post and retiveing all post
class PostListCreateView(GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['title', 'content']
    search_fields = ['title', 'content']

    def get(self, request):
        post_objects = self.filter_queryset(self.get_queryset())
        serializer = PostSerializer(post_objects, many=True)
        return Response({'data': serializer.data})

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': "post created successfully"})
        return Response({'error':serializer.errors})
    

# get singal post detail, update , delete
class PostDetailView(GenericAPIView):
    queryset_model = Post
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get(self, request, pk):
        post_objects = Post.objects.get(id=pk)
        serializer = self.get_serializer(post_objects)
        return Response({'data': serializer.data})

    def put(self, request, pk):
        post_objects = Post.objects.get(id=pk)
        self.check_object_permissions(request, post_objects)
        serializer = self.get_serializer(post_objects, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': "Post Updated Successfull"})
        return Response({'error':serializer.errors})

    def delete(self, request, pk):
        post_objects = Post.objects.get(id=pk)
        self.check_object_permissions(request, post_objects)
        post_objects.delete()
        return Response({'message': 'Data deleted successfull'})
    

#creating commet and retiveing all comment
class CommentListCreateView(GenericAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['post', 'text']
    search_fields = ['post', 'text']

    def get(self, request):
        comment_objects = self.filter_queryset(self.get_queryset())
        serializer = CommentSerializer(comment_objects, many=True)
        return Response({'data': serializer.data})

    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data})
        return Response({'error':serializer.errors})
    
    
# get singal comment detail, update , delete
class CommentDetailView(GenericAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get(self, request, pk):
        comment_objects = Comment.objects.get(id=pk)
        serializer = self.get_serializer(comment_objects)
        return Response({'data': serializer.data})

    def put(self, request, pk):
        comment_objects = Comment.objects.get(id=pk)
        # checking isownerorreadonly to perform update operation
        self.check_object_permissions(request, comment_objects)
        serializer = self.get_serializer(comment_objects, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': "comment Updated Successfully!"})
        return Response({'error':serializer.errors})

    def delete(self, request, pk):
        comment_objects = Comment.objects.get(id=pk)
        # checking isownerorreadonly to perform delete operation
        self.check_object_permissions(request, comment_objects)
        comment_objects.delete()
        return Response({'message': 'Data deleted successfull'})
    
    
# Retiveing all like
class LikeListCreateView(GenericAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        like_Objects = self.get_queryset()
        serializer = LikeSerializer(like_Objects, many=True)
        return Response({'data': serializer.data})

    def post(self, request):
        serializer = LikeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data})
        return Response({'error':serializer.errors})
    
    
# Retriving singal like
class LikeDetailView(GenericAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get(self, request, pk):
        like_objects = Like.objects.get(id=pk)
        serializer = self.get_serializer(like_objects)
        return Response({'data': serializer.data})

    def put(self, request, pk):
        like_objects = Like.objects.get(id=pk)
        # checking isownerorreadonly to perform update operation
        self.check_object_permissions(request, like_objects)
        serializer = self.get_serializer(like_objects, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': "Profile Updated Successfull"})
        return Response({'error':serializer.errors})

    def delete(self, request, pk):
        like_objects = Like.objects.get(id=pk)
        # checking isownerorreadonly to perform delete operation
        self.check_object_permissions(request, like_objects)
        like_objects.delete()
        return Response({'message': 'Data deleted successfull'})
    
        
#implementing activity feed which retrive recent post, comment, like, from friends
class ActivityFeedView(GenericAPIView):
    serializer_class = serializers.Serializer
    permission_classes = [IsAuthenticated]

    # def getPosts(self,friends):
    #     posts = Post.objects.filter(user__in=friends).all()[:5]
    #     postSerializer = PostSerializer(posts, many=True)
    #     return postSerializer.data
    
    

    def get(self, request, *args, **kwargs):
        user = self.request.user
        # print(user)
        friends = Friendship.objects.filter(user=user).values_list('friend', flat=True)
        # retriving 2 recently posted  
        posts = Post.objects.filter(user__in=friends).order_by('-created_at')[:5]
        postSerializer = PostSerializer(posts, many=True)
        # retriving 2 recently commented 
        comments = Comment.objects.filter(user__in=friends).order_by('-created_at')[:5]
        commentSerializer = CommentSerializer(comments, many=True)
        # retriving 2 recently liked 
        likes = Like.objects.filter(user__in=friends).order_by('-created_at')[:5]
        likeSerializer = LikeSerializer(likes, many=True)

       
        return Response({
            'posts':postSerializer.data,
            'comments':commentSerializer.data,
            'likes':likeSerializer.data,
        })
        
        