from django.db import models

# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=50)
    director = models.CharField(max_length=50)
    actors = models.CharField(max_length=150)
    genre = models.CharField(max_length=50)
    release_date = models.DateField()
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    runningtime = models.IntegerField()
    review_text = models.TextField()
    poster = models.ImageField(upload_to='posters/', blank=True, null=True)  # 포스터 이미지 필드 추가

    # __str__는 그 객체를 대표하는 이름표를 붙여주는 것
    def __str__(self):
        return self.title