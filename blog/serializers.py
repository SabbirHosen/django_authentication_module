from rest_framework import serializers
from .models import Blog, Comment

class BlogSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = ['id', 'title', 'slug', 'content', 'summary','author', 'created_at', 'updated_at', 'tags', 'category', 'likes_count']

    def get_likes_count(self, obj):
        return obj.likes.count()

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'blog', 'author_name', 'author_email', 'content', 'created_at']

    def create(self, validated_data):
        """
        Handle anonymous comments by saving the provided name and email.
        """
        return Comment.objects.create(**validated_data)
