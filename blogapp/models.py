from django.db import models

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    autor = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='articles_authored')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    autor = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='comments_authored')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if len(self.content) > 30:
           return f'Commentaire par {self.autor.username} sur "{self.article.title}" : "{self.content[:30]}..."'
        return f'Commentaire par {self.autor.username} sur "{self.article.title}" : "{self.content}"'
    
    class Meta:
       ordering = ['created_at']