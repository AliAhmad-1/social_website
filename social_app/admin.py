from django.contrib import admin

from .models import Post, Comment ,Action


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'content', 'image', 'created', 'updated')
    list_filter = ('user', 'created', 'updated')
    raw_id_fields = ('saves', 'likes')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'user', 'content', 'created', 'updated')
    list_filter = ('post', 'user', 'created', 'updated')

@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'verb',
        'created',
        'target_ct',
        'target_id',
    )
    list_filter = ('user', 'created', 'target_ct')