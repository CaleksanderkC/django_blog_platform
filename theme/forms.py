from django import forms
from theme.models import Post, Comment


class PostModelCreat(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['post_title', 'post_text']
        widgets = {
            'post_title': forms.Textarea(attrs={'rows': 2,
                                                'cols': 103,
                                                'class': "form-control ",
                                                'id': "inputdefault",
                                                }),
            'post_text': forms.Textarea(attrs={'rows': 30,
                                               'cols': 103,
                                               'class': "form-control input-lg creat-text",
                                               'id': "inputlg",
                                               })
        }
        labels = {
            'post_title': "Post Title",
            'post_text': 'Post Text'
        }


class CommentModelForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_text']
        widgets = {
            'comment_text': forms.Textarea(attrs={
                'rows': 2,
                'cols': 100,
                'class': "form-control input-sm"
            })
        }


# class UserProfile(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ['username', 'password']

