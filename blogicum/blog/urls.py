from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='index'),
    path(
        'posts/<int:pk>/',
        views.PostDetailView.as_view(),
        name='post_detail'
    ),
    path(
        'category/<slug:category_slug>/',
        views.CategoryPostListView.as_view(),
        name='category_posts'
    ),
    path(
        'profile/<str:username>/',
        views.ProfileListView.as_view(),
        name='profile'
    ),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('posts/create/', views.create_post, name='create_post'),
    path('posts/<int:pk>/edit/', views.edit_post, name='edit_post'),
    path('posts/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path(
        'posts/<int:pk>/edit_comment/<int:comment_id>/',
        views.edit_comment,
        name='edit_comment'
    ),
    path(
        'posts/<int:pk>/delete_comment/<int:comment_id>/',
        views.delete_comment,
        name='delete_comment'
    ),
]
