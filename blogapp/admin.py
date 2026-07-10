from django.contrib import admin

from blogapp.models import Article, Comment

# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'autor', 'created_at', 'updated_at')
    search_fields = ('title', 'content', 'autor__username')
    list_filter = ('created_at', 'updated_at', 'autor')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('article', 'autor', 'short_content', 'created_at', 'updated_at')
    search_fields = ('content', 'autor__username', 'article__title')
    list_filter = ('created_at', 'updated_at', 'autor')

    def short_content(self, obj):
        if len(obj.content) > 30:
            return f'{obj.content[:30]}...'
        return obj.content

admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)