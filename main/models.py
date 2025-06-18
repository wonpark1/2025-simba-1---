from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Tag(models.Model):
    tag_name = models.CharField(max_length=8)

    def __str__(self):
        return self.tag_name

class LookCard(models.Model):
    LookId = models.IntegerField(null=False, blank=False)
    Lookname = models.CharField(max_length=8)
    LookImg = models.ImageField(upload_to="post/", blank=False, null=False)
    LookEXP = models.TextField()
    Look_MaxTemp = models.FloatField()
    Look_MinTemp = models.FloatField()
    tags = models.ManyToManyField(Tag, related_name="LookTags", blank=False)
    likes = models.IntegerField()

    def __str__(self):
        return self.Lookname