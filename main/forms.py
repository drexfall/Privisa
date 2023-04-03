from django import forms
from .models import User, PasswordEntry, GeneratorSettings


class Login(forms.ModelForm):

    class Meta:
        model = User
        fields = ['password']

    def __init__(self, *args, **kwargs):
        super(Login, self).__init__(*args, **kwargs)

        self.fields['password'].label = ""
        self.fields['password'].widget = forms.PasswordInput(
            attrs={'placeholder': 'Enter password'})


class PasswordInput(forms.ModelForm):

    class Meta:
        model = PasswordEntry
        fields = ['website', 'username', 'password']

    def __init__(self, *args, **kwargs):
        super(PasswordInput, self).__init__(*args, **kwargs)

        self.fields['website'].label = ""
        self.fields['website'].widget = forms.TextInput(
            attrs={'placeholder': 'Enter website'})
        self.fields['username'].label = ""
        self.fields['username'].widget = forms.TextInput(
            attrs={'placeholder': 'Enter username'})
        self.fields['password'].label = ""
        self.fields['password'].widget = forms.PasswordInput(
            attrs={'placeholder': 'Enter password'})


class SettingsForm(forms.ModelForm):
    class Meta:
        model = GeneratorSettings
        exclude = []

    def __init__(self, *args, **kwargs):
        super(SettingsForm, self).__init__(*args, **kwargs)
        settings = GeneratorSettings.objects.get(id=1)
        if (settings.digits):
            self.fields['digits'].widget.attrs = {'checked': settings.digits}

        if (settings.alphabets):
            self.fields['alphabets'].widget.attrs = {'checked': settings.alphabets}

        if (settings.punctuations):
            self.fields['punctuations'].widget.attrs = {
                'checked': settings.punctuations}

        if (settings.uppercase):
            self.fields['uppercase'].widget.attrs = {'checked': settings.uppercase}

        self.fields['length'].initial = settings.length
