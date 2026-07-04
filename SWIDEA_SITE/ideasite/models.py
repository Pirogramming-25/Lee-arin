from django.db import models
from django.conf import settings

# Create your models here.
class Devtool(models.Model):
    dev_name = models.CharField(max_length=100)
    dev_kind = models.CharField(max_length=100)
    dev_content = models.TextField()

    def __str__(self):
        return self.dev_name
    
class Idea(models.Model):
    # 직접 입력
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    interest = models.IntegerField(default=0)
    devtool = models.ForeignKey(
        Devtool,
        on_delete=models.CASCADE,
        related_name='ideas',
    )

    # 알아서 저장됨
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class IdeaStar(models.Model):
    session_key = models.CharField(max_length=100)   # user 대신
    idea = models.ForeignKey(
        Idea,
        related_name='idea_stars',
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['session_key', 'idea'],
                name='unique_session_idea_star',
            )
        ]