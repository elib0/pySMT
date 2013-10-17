from django import forms


class LoginForm(forms.Form):
    name = forms.CharField(max_length=30, min_length=5, required=True, label='Nombre')
    password = forms.CharField(widget=forms.PasswordInput(),
                               label='Contrasena',
                               max_length=30, min_length=6)
