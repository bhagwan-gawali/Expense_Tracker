from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class RegisterForm(forms.ModelForm):
    """New User Registraion Form using built in django.contrib.auth.models"""
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password',]

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'email': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control form-control-sm',}),
        }

    def clean_username(self):
        data = self.cleaned_data.get('username')
        try:
            u_name = User.objects.get(username__exact=data)
            if u_name.username:
                self.add_error('username', f'{u_name.username} is already taken please use diffrent one..')
        except:
            pass

        return data


    def clean_email(self):
        data = self.cleaned_data.get('email')
        try:
            e_mail = User.objects.get(email__exact=data)
            if e_mail.email:
                self.add_error('email', f'{e_mail.email} is already taken please use diffrent one..')
        except:
            pass

        return data

    # def clean(self):
    #     """clean method for extra validation check."""
    #     data = self.cleaned_data
    #     print("My data : ", data)

    #     try:
    #         u_name = User.objects.get(username=data.get('username'))
    #         print("U_data : ", u_name)
    #         if u_name.username:
    #             self.add_error('username', f'{u_name.username} is already taken please use diffrent one..')
    #     except:
    #         # self.add_error('username', f'username is already taken please use diffrent one..')
    #         pass

    #     try:
    #         e_mail = User.objects.get(email__exact=data.get('email'))
            
    #         if e_mail.email:
    #             self.add_error('email', f'{e_mail.email} is already taken please use diffrent one..')
    #     except:
    #         # self.add_error('username', f'username is already taken please use diffrent one..')
    #         pass

    #     return data

class LoginForm(forms.ModelForm):
    """User Login Form Using build in django.contrib.auth.models"""
    class Meta:
        model = User
        fields = ['username', 'password']

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control form-control-sm',}),
        }

    def clean(self):
        data = self.cleaned_data

