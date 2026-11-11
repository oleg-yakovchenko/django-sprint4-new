from django import forms
from django.core.exceptions import ValidationError

from .models import Comment, Post
from .moderation import is_toxic

MODERATION_ERROR = (
    'Комментарий не проходит модерацию. '
    'Пожалуйста, сформулируйте мысль корректнее.'
)


class PostForm(forms.ModelForm):
    """Форма создания и редактирования публикации."""

    class Meta:
        model = Post
        exclude = ('author', 'created_at')
        widgets = {
            'pub_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M',
            ),
        }


class CommentForm(forms.ModelForm):
    """Форма комментария: только текст + проверка модерации."""

    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }

    def clean_text(self):
        text = self.cleaned_data['text']
        if is_toxic(text):
            raise ValidationError(MODERATION_ERROR)
        return text
