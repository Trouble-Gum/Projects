from apps.adverts.models import Post, Author
from django import forms
from martor.fields import MartorFormField


class NewForm(forms.ModelForm):
    caption = forms.CharField(min_length=20)
    author = forms.ModelChoiceField(queryset=Author.objects.all())
    description = MartorFormField()

    class Meta:
        model = Post
        fields = [
            'author',
            'caption',
            'post_type',
            'description'
        ]
