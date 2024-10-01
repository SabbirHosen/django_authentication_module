from rest_framework import generics, status
from .models import Blog, Comment
from .serializers import BlogSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework.response import Response

# List and detail views for Blog
class BlogListView(generics.ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'tags']

class BlogDetailView(generics.RetrieveAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    lookup_field = 'slug'

# Create and list comments
class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]  # Allow anonymous users to post

    def get_queryset(self):
        """
        This method will return comments related to a specific blog.
        """
        blog_id = self.kwargs.get('blog_id')  # or use 'slug' if your blog uses slugs
        return Comment.objects.filter(blog__id=blog_id)

    def perform_create(self, serializer):
        """
        Save a new comment, either from an authenticated or anonymous user.
        """
        blog_id = self.kwargs.get('blog_id')
        blog = Blog.objects.get(id=blog_id)  # Get the blog instance

        # Save the comment and associate it with the correct blog
        serializer.save(blog=blog)

# Handle liking/unliking blogs
@api_view(['POST'])
def like_blog(request, slug):
    blog = Blog.objects.get(slug=slug)
    user = request.user
    if blog.likes.filter(id=user.id).exists():
        blog.likes.remove(user)
        return Response({'message': 'You have unliked this post'}, status=200)
    else:
        blog.likes.add(user)
        return Response({'message': 'You have liked this post'}, status=200)
