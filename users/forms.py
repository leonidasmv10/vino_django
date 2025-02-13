from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "password"]
        widgets = {
            "password": forms.PasswordInput(),
        }
        error_messages = {
            "username": {
                "required": "El nombre de usuario es obligatorio.",
                "max_length": "El nombre de usuario no puede tener más de 150 caracteres.",
                "invalid": "El nombre de usuario solo puede contener letras, dígitos y los símbolos @/./+/-/_.",
            },
            "password": {
                "required": "La contraseña es obligatoria.",
            },
        }
