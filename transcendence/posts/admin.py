from posts.models import Post

from django.contrib import admin


class BookmarkInlineAdmin(admin.TabularInline):
    model = Post.bookmarked.through

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'post_date')
    fieldsets = (
        ('Info', {'fields': ('name', 'author', 'description', 'post_date')}),
        )

    inlines = (BookmarkInlineAdmin,)
