from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Comment, Profile, Category

# User Registration Form
class UserSignupForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}))
    first_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'password1' in self.fields:
            self.fields['password1'].label = 'Password'
        if 'password2' in self.fields:
            self.fields['password2'].label = 'Confirm Password'

        for field in self.fields:
            if field != 'email' and field != 'first_name' and field != 'last_name':
                self.fields[field].widget.attrs.update({'class': 'form-control', 'placeholder': self.fields[field].label})


# User Details Update Form
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


# Profile details update (avatar, bio, website)
class ProfileUpdateForm(forms.ModelForm):
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Tell us something about yourself...'}))
    website = forms.URLField(required=False, widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://yourwebsite.com'}))
    avatar = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control-file'}))

    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'website']


# Post Creation and Edit Form
class PostForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter post title...'}))
    banner = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 12, 'placeholder': 'Write your story in markdown format...'}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Select Category", widget=forms.Select(attrs={'class': 'form-select'}))
    status = forms.ChoiceField(choices=Post.STATUS_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = Post
        fields = ['title', 'banner', 'content', 'category', 'status']


# Comment Creation Form
class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'rows': 3,
        'placeholder': 'Share your thoughts on this story...',
        'id': 'commentContentField'
    }))

    class Meta:
        model = Comment
        fields = ['content']
