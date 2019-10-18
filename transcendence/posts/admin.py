from posts.models import Post

from django.contrib import admin

@admin.register(Post)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'post_date')
