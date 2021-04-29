from django.db import models
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
        default=timezone.now()
    )
    published_date = models.DateTimeField(
        blank=True, null=True
    )

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.TextField(max_length=500)
    created_by = models.CharField(max_length=25, default='Guest', null=True)
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, null=True)
    created_date = models.DateTimeField(default=timezone.now())
    published_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        default_related_name = 'comments'

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return f"Comment by {self.created_by}"
