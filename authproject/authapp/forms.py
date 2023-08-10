from django import forms
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
# from django.contrib.auth.models import User
# from django.utils.translation import gettext, gettext_lazy as _
from .models import Post



class PostForm(forms.ModelForm):
  class Meta:
    model = Post
    fields = ['title', 'desc']
    labels = {'title':'Title', 'desc':'Description'}
    widgets = {'title':forms.TextInput(attrs={'class':'form-control'}),
    'desc':forms.Textarea(attrs={'class':'form-control'}), }