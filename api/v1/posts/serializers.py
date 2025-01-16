from rest_framework import serializers
from posts.models import *
from accounts.models import *

class PostSerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    profile_photo = serializers.SerializerMethodField()
    school_name = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    is_saved = serializers.SerializerMethodField()
    date_added = serializers.SerializerMethodField()


    class Meta:
        model = Post
        fields = (
            'id',
            'user_id',
            'name',
            'profile_photo',
            'school_name',
            'title',
            'description',
            'image',
            'like_count',
            'is_liked',
            'comment_count',
            'is_saved',
            'date_added'
        )

    def get_like_count(self, obj ):
        return obj.like.count()
    
    def get_name(self,obj):
        return obj.user.name
    
    def get_profile_photo(self, obj):
        request = self.context.get('request')  # Get the request from context
        if obj.user.image:
            return request.build_absolute_uri(obj.user.image.url)  # Get absolute URL
        return None
    
    def get_school_name(self,obj):
        return obj.user.school_name.name
    
    def get_user_id(self,obj):
        return obj.user.id
    
    def get_is_liked(self, obj):
        user = self.context['request'].user  
        return obj.like.filter(user=user).exists()
    
    def get_comment_count(self, obj):
        return obj.comment_set.count()
    
    def get_is_saved(self, obj):
        user = self.context['request'].user  
        return obj.saved_by.filter(user=user).exists()
    
    def get_date_added(self, obj):
        return obj.date_added.strftime("%b %d, %Y")


    
class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'description', 'image']

    def create(self, validated_data):
        request = self.context.get('request')
        if not request:
            raise ValueError("Request object is required.")

        user_profile = request.user.userprofile
        post = Post(user=user_profile, **validated_data)
        post.save() 
        return post
    

class CommentSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    profile_photo = serializers.SerializerMethodField()
    school_name = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = (
            'id',
            'comment_text',
            'user_name',
            'profile_photo',
            'school_name',
            
        )
    
    def get_user_name(self,obj):
        return obj.user.name
    
    def get_profile_photo(self, obj):
            request = self.context.get('request')  # Get the request from context
            if obj.user.image:
                return request.build_absolute_uri(obj.user.image.url)  # Get absolute URL
            return None
    
    def get_school_name(self,obj):
        return obj.user.school_name.name
    

class AddCommentSerializer(serializers.ModelSerializer):
     
     class Meta:
        model = Comment
        fields = (
            'comment_text', 
        )


class SchoolSerializer(serializers.ModelSerializer):
     
     class Meta:
        model = School
        fields = (
            'id',
            'name', 
        )


class SavedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'description', 'image']