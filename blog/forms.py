from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import User, Comment


class UserCreationForm(forms.ModelForm):
    email     = forms.CharField(max_length=30, label='Adresse e-mail', widget=forms.TextInput(
    attrs={'class': 'input[type=email]'}))
    username  = forms.CharField(max_length=20, label="Nom d'utilisateur", widget=forms.TextInput(
    attrs={'class': 'input[type=text]'}))
    password1 = forms.CharField(max_length=10, label='Mot de passe', widget=forms.PasswordInput(
    attrs={'class': 'input[type=password]'}))
    password2 = forms.CharField(max_length=10, label='Confirmation de mot de passe', widget=forms.PasswordInput(
    attrs={'class': 'input[type=password]'}))

    class Meta:
        model = User
        fields = ('email', 'username',)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'username',
                  'is_active', 'is_admin')

    def clean_password(self):
        return self.initial["password"]


class CommentForm(forms.ModelForm):
    content = forms.CharField(label ="", widget = forms.Textarea(
    attrs ={
        'class':'form-control',
        'placeholder':'Veuillez écrire votre commentaire',
        'rows':4,
        'cols':50
    }))
    class Meta:
        model = Comment
        fields =['content']


class ContactForm(forms.Form):
    
    name = forms.CharField(max_length=80, label="Nom", widget=forms.TextInput(
    attrs={'class': 'input[type=text]'}))
    
    subject = forms.CharField(max_length=100, label="Objet", widget=forms.TextInput(
    attrs={'class': 'input[type=text]'}))
    
    sender = forms.EmailField(label="Adresse e-mail", widget=forms.TextInput(
    attrs={'class': 'input[type=email]'}))
    
    message = forms.CharField(widget=forms.Textarea(
    attrs={'placeholder': 'Veuillez saisir votre message'}))