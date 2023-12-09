from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('users/', UserListCreateView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('profiles/', ProfileListCreateView.as_view(), name='profile-list'),
    path('profiles/<int:pk>/', ProfileDetailView.as_view(), name='profile-detail'),
    path('posts/', PostListCreateView.as_view(), name='post-list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('comments/', CommentListCreateView.as_view(), name='comment-list'),
    path('comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
    path('likes/', LikeListCreateView.as_view(), name='like-list'),
    path('likes/<int:pk>/', LikeDetailView.as_view(), name='like-detail'),
]
