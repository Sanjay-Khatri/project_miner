from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Post(models.Model):

    filter_choices = (
("Artificial Intelligence","Artificial Intelligence"),
("Internet of things","Internet of things"),
("Web App","Web App"),
("Android","Android"),
("Games","Games"),
("others..","others.."),
    )

    title = models.CharField(max_length=30)
    category = models.CharField(max_length=30,choices = filter_choices)
    user= models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    summary = models.CharField(max_length=100)
    image =models.ImageField(upload_to = 'images/')
    pub_date = models.DateTimeField()
    body = models.TextField()
    earn = models.DecimalField(max_digits=12,decimal_places=8,default=0)

    def __str__(self):
        return self.title

    def description(self):
        return self.body[:200]


class Comment(models.Model):
    post_name = models.ForeignKey('Post', on_delete=models.CASCADE, null=True)
    author = models.CharField(max_length=30, null=True)
    body = models.TextField()
    pub_date = models.DateTimeField()


class Reaction(models.Model):
    post_name = models.ForeignKey('Post', on_delete=models.CASCADE, null=True)
    user = models.CharField(max_length=30, null=True)
    upvote = models.IntegerField(default=0)
    report = models.IntegerField(default=0)

    def __str__(self):
        return self.user
