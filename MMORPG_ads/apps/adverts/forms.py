from django.core.exceptions import ValidationError

from django import forms
from apps.adverts.models import Post, Author
import datetime as dt


class NewForm(forms.ModelForm):
    caption = forms.CharField(min_length=20)
    text = forms.CharField(widget=forms.Textarea(attrs={'name': 'body', 'rows': 10, 'cols': 100}))
    author = forms.ModelChoiceField(queryset=Author.objects.all())

    class Meta:
        model = Post
        fields = [
            'author',
            'caption',
            'text',
            'categories'
        ]

    def clean(self):
        cleaned_data = super().clean()
        caption = cleaned_data.get("caption")
        text = cleaned_data.get("text")
        author = cleaned_data.get("author")
        today = dt.date.today()
        posts = Post.objects.filter(author=author, posted_at__date=today).count()
        if posts >= 3:
            raise ValidationError("Limit on amount of posts is 3 posts a day per one author")
        if caption == text:
            raise ValidationError(
                "text shouldn't be equal to caption."
            )

        return cleaned_data

    # def is_valid(self):
    #     print(self.data)
    #     # self.author = Author.objects.get(pk=self.data['author'])
    #     super().is_valid()
    #     # raise Exception("!!! !!! !!!")


class NewArticle(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['author', 'caption', 'text']
