from django import forms
from models import Topic, Comment


class CommentForm(forms.Form):
    body = forms.CharField(label='Your Comment')

    class Meta():
        model = Comment
        exclude = ('updated', 'created','topic')
