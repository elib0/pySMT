from django import forms


class LoginForm(forms.Form):
    name = forms.CharField(max_length=30, min_length=5, required=True, label='Nombre')
    password = forms.CharField(widget=forms.PasswordInput(),
                               label='Contrasena',
                               required=True,
                               max_length=30, min_length=6)


class RegisterForm(forms.Form):
    name = forms.CharField(max_length=30, min_length=5, required=True, label='Nombre')
    email = forms.CharField(max_length=100,
                            min_length=10,
                            required=True,
                            label='Correo Electronico')
    password = forms.CharField(widget=forms.PasswordInput(),
                               label='Contrasena',
                               max_length=30, min_length=6)
    repassword = forms.CharField(widget=forms.PasswordInput(),
                                 label='Repite Contrasena',
                                 max_length=30, min_length=6)

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get('password')
        repassword = cleaned_data.get('repassword')
        if password != repassword:
            raise forms.ValidationError("Las contrasenas no son iguales")
        return cleaned_data
