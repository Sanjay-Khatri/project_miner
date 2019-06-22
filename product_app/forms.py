from django import forms
from .models import Post, Comment
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm


class PostForm(forms.ModelForm):

    filter_choices = (
("Artificial Intelligence","Artificial Intelligence"),
("Internet of things","Internet of things"),
("Web App","Web App"),
("Android","Android"),
("Games","Games"),
("others..","others.."),
    )

    category = forms.ChoiceField(choices = filter_choices)
    image = forms.ImageField()

    class Meta:
        model = Post
        fields = ('title','summary','body')
        exclude = ( 'pub_date','user',)
        required = ('title', 'summary', 'body', 'category', 'image')



class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('body', )
        exclude = ('author', 'post_name','pub_date',)
        required = ('body',)


class editProfileForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')
