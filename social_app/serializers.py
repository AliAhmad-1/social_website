from .models import Post,Comment
from accounts.models import MyUser
from rest_framework import serializers
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('id', 'username')
class CommentSerializer(serializers.ModelSerializer):
    post_id= serializers.ReadOnlyField(source='post.id')
    username = serializers.CharField(source='user.username', read_only=True)
    user_id = serializers.ReadOnlyField(source='user.id')
    image_profile = serializers.ImageField(source='user.image_profile', read_only=True)
    created=serializers.DateTimeField(format='%h %d, %Y, %H:%m')
  
    class Meta:
        model=Comment
        fields=('id','content','username','created','image_profile','user_id','post_id')
class PostSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    user_id = serializers.ReadOnlyField(source='user.id')
    image_profile = serializers.ImageField(source='user.image_profile', read_only=True)
    created=serializers.DateTimeField(format='%h %d, %Y, %H:%m')
    likes = UserSerializer(many=True, read_only=True)
    saves= UserSerializer(many=True, read_only=True)
    post_comments = CommentSerializer(many=True, read_only=True)
   
    
    class Meta:
        model = Post
        fields = ('id','content', 'image', 'username', 'user_id', 'image_profile', 'created','likes','saves','post_comments')

