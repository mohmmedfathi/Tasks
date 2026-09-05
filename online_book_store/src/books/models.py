from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    author = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    content = models.TextField()
    published_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
