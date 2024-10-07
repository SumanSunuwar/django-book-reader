from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from apps.reader.models import ReadingList


class UserAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget = forms.TextInput(attrs={'class': 'bg-green-100 shadow-inner w-full border-solid py-2 px-3', 'placeholder': 'Username'}))
    password = forms.CharField(widget = forms.PasswordInput(attrs={'class': 'bg-green-100 shadow-inner w-full border-solid py-2 px-3', 'placeholder': 'Password'}))
    class Meta:
        model = User
        fields = ('username','password')
    

class ReaderRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'bg-green-100 shadow-inner w-full border-solid py-2 px-3'}),
        required=True  
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'bg-green-100 shadow-inner w-full border-solid py-2 px-3'})
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'bg-green-100 shadow-inner w-full border-solid py-2 px-3'})
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'bg-green-100 shadow-inner w-full border-solid py-2 px-3'})
    )

    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(ReaderRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class ReadingListForm(forms.ModelForm):
    class Meta:
        model = ReadingList
        fields = ['status']