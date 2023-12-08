import mistune
from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.safestring import mark_safe

from app_posts.models import AppPost
from authors.models import Author
from comments.models import Comment


# post form to add a post
class AppPostForm(forms.ModelForm):
    """Form for adding a post"""

    friends_to_notify = forms.ModelMultipleChoiceField(
        queryset=Author.objects.none(),  # Leave it empty for now
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Friends to Notify",
        help_text="Select friends to notify",
    )

    def __init__(self, *args, **kwargs):
        # Fetch the user's friends and set the queryset for friends_to_notify field
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if user:
            friend_ids = user.friends.all().values_list("id", flat=True)
            followers_ids = user.followers.all().values_list("id", flat=True)
            foreign_authors_ids = []
            if user.foreign_authors:
                foreign_authors_ids = [
                    str(author["id"]) for author in user.foreign_authors
                ]

            friends_queryset = Author.objects.filter(id__in=friend_ids)
            followers_queryset = Author.objects.filter(id__in=followers_ids)
            foreign_authors_queryset = Author.objects.filter(id__in=foreign_authors_ids)

            # Combine all queryset
            all_queryset = (
                friends_queryset | followers_queryset | foreign_authors_queryset
            )

            self.fields["friends_to_notify"].queryset = all_queryset

    class Meta:
        fields = [
            "title",
            "description",
            "contentType",
            "content",
            "categories",
            "visibility",
            "image",
            "friends_to_notify",
            "unlisted",
        ]
        image = forms.FileField(required=False)
        unlisted = forms.BooleanField(required=False)
        model = AppPost

        widgets = {
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "friends_to_notify": forms.CheckboxSelectMultiple(
                attrs={"class": "friends-to-notify"}
            ),
        }


class CommentForm(forms.ModelForm):
    """Form for adding a comment"""

    # need to specify model for form to recognise and allow editing
    class Meta:
        model = Comment
        fields = ["contentType", "content"]
        model = Comment

        widgets = {
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }


# convert plaint text to common mark
def toCommonMark(plain):
    """Convert plain text to common mark"""
    # Markdown rendering
    markdown = mistune.markdown(plain)
    return mark_safe(markdown)


# post form to register authors
class AuthorRegistrationForm(UserCreationForm):
    """Form for registering authors"""

    class Meta:
        model = Author
        fields = ["username", "github"]  # password auto needed/required

        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "password": forms.PasswordInput(attrs={"class": "form-control"}),
            "github": forms.TextInput(attrs={"class": "form-control"}),
        }


class AuthorEditForm(forms.ModelForm):
    """Form for editing authors"""

    class Meta:
        model = Author
        fields = ["username", "github"]  # password auto needed/required

        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "github": forms.TextInput(attrs={"class": "form-control"}),
        }


class AuthorLoginForm(forms.ModelForm):
    """Form for logging in authors"""

    class Meta:
        model = Author
        fields = ["username", "password"]
        fields = ["username", "github"]  # password auto needed/required
