from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Month(models.Model):
    number = models.IntegerField()
    
    def __str__(self):
        return f"{self.number}월"

class Tag(models.Model):
    name=models.CharField(max_length=30, null=False, blank=False)

    def __str__(self):
        return self.name

class Event(models.Model):
    title = models.CharField(max_length=15)
    month = models.ManyToManyField(Month, related_name="month", blank=True)
    description_main = models.TextField(blank=False, null=False)
    description_look = models.TextField(blank=True, null=True)
    mention = models.TextField(blank=False, null=False)
    emoticon = models.ImageField(upload_to='emoticons/', blank=True, null=True)
    start = models.IntegerField()
    end = models.IntegerField()

    def __str__(self):
        months = ", ".join([str(m) for m in self.month.all()])
        return f"{months}_{self.title}"

class LookCard(models.Model):
    event = models.ForeignKey(Event, related_name='lookcards', on_delete=models.CASCADE)
    month = models.ForeignKey(Month, related_name='lookcards', on_delete=models.CASCADE, null=True, blank=True)
    is_recommend = models.TextField(blank=False)
    is_avoid = models.TextField(blank=False)
    avoid_reason = models.TextField(blank=False)

    def __str__(self):
        return self.event.title
    
class LookItem(models.Model):
    CATEGORY_CHOICES = [
        ('상의', '상의'),
        ('하의', '하의'),
        ('악세서리', '악세서리'),
    ]

    look_card = models.ForeignKey(LookCard, related_name='items', on_delete=models.CASCADE)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    name = models.CharField(max_length=100, blank=True, null=True)
    tags = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Comment(models.Model):
    look_card = models.ForeignKey(LookCard, related_name='comments', on_delete=models.CASCADE)
    writer = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='comment_images/', blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)

    tags = models.ManyToManyField(Tag, related_name='tags', blank=True)

    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    dislikes = models.ManyToManyField(User, related_name='dislikes', blank=True)

    def __str__(self):
        return f"{self.content[:20]} by {self.writer.username}"
