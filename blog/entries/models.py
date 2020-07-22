from django.contrib.auth.models import User
from django.db import models


class Entry(models.Model):
    entry_title = models.CharField(max_length=50)
    entry_text = models.TextField()
    entry_date = models.DateTimeField(auto_now_add=True)
    entry_author = models.ForeignKey(User, on_delete = models.CASCADE)
    entry_likes = models.ManyToManyField(User, related_name= 'likes', blank=True)
    
    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        return self.entry_title



class Comment(models.Model):
    comment_author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    comment_text = models.TextField(blank=True, null=True)
    comment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment_author.username + " " + self.comment_entry.entry_title

    class Meta:
        verbose_name_plural = 'comments'
