from django.core.exceptions import ValidationError

from django import forms
from apps.news.models import Post


class NewForm(forms.ModelForm):
    caption = forms.CharField(min_length=20)

    class Meta:
        model = Post
        fields = [
            'author',
            'caption',
            'text'
        ]

    def clean(self):
        cleaned_data = super().clean()
        caption = cleaned_data.get("caption")
        text = cleaned_data.get("text")

        if caption == text:
            raise ValidationError(
                "text shouldn't be equal to caption."
            )

        return cleaned_data


class NewArticle(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['author', 'caption', 'text']