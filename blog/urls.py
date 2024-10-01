from django.urls import path
from .views import BlogListView, BlogDetailView, CommentListCreateView, like_blog

app_name = "blog"

urlpatterns = [
    path('', BlogListView.as_view(), name='blog-list'),
    path('<slug:slug>/', BlogDetailView.as_view(), name='blog-detail'),
    path('<slug:slug>/like/', like_blog, name='like-blog'),
    path('<int:blog_id>/comments/', CommentListCreateView.as_view(), name='blog-comments'),
]
