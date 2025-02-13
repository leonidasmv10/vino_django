from django import forms
from .models import Wine


class WineAdminForm(forms.ModelForm):
    class Meta:
        model = Wine
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:  # Si el vino no está guardado (nuevo)
            self.fields["name"].initial = "Vino Automático"
            self.fields["description"].initial = "Descripción automática."
            self.fields["price"].initial = 20.00
            self.fields["category"].initial = (
                1  # Asigna la categoría con ID 1 (ajusta según tu base de datos)
            )
            # Aquí puedes asignar los valores predeterminados para otros campos
