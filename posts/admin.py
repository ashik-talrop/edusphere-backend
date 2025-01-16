from django.contrib import admin
from .models import *

class PostAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'user', 'like_count', 'creator', 'date_added', 'is_deleted')
    search_fields = ('title', 'user__name', 'description')
    list_filter = ('date_added', 'date_updated', 'is_deleted')
    ordering = ('-date_added',)

    def like_count(self, obj):
        return obj.like.count()
    like_count.short_description = 'Likes'

admin.site.register(Post,PostAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id','comment_text', 'creator','post','is_deleted')
    search_fields = ('post__title', 'comment_text')
    list_filter = ('date_added', 'date_updated', 'is_deleted')
    ordering = ('-date_added',)

admin.site.register(Comment,CommentAdmin)


