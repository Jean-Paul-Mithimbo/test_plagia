# # forms.py
# from django import forms
# from .models import UserDocument

# class UserDocumentForm(forms.ModelForm):
#     class Meta:
#         model = UserDocument
#         fields = ['title', 'pdf']


from django import forms
from .models import UserDocument
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class UserDocumentForm(forms.ModelForm):
    class Meta:
        model = UserDocument
        fields = ['title', 'pdf']

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Nom d'utilisateur", max_length=254)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)
