from django import forms
from .models import Wine
from wines.services import generate_text
import json


class WineAdminForm(forms.ModelForm):
    class Meta:
        model = Wine
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:

            prompt = """
Genera un vino aleatorio y responde siempre con una matriz JSON que incluya las siguientes propiedades:

- "name" (texto): Un nombre creativo de entre 25 y 35 caracteres.
- "description" (texto): Una descripción ingeniosa y evocadora.
- "category" (entero):
  - 1 = Tinto (Fuego)
  - 2 = Blanco (Nieve)
  - 3 = Rosado (Agua)
- "body", "aroma", "taste", "tannins", "acidity", "sweetness", "aging" (enteros del 1 al 10): Valores sensoriales del vino.
- "price" (decimal): Se calcula en función de las propiedades sensoriales.
- "total_score" (promedio de body, aroma, taste, tannins, acidity, sweetness y aging).

### **Probabilidad de generación del nombre y reglas de "total_score":**
- **40% de probabilidad**: Generar un nombre **débil o sin respeto** → `total_score` **entre 1 y 2** (propiedades entre **1 y 3**).
- **30% de probabilidad**: Generar un nombre **neutro o estándar** → `total_score` **entre 3 y 4** (propiedades entre **3 y 5**).
- **20% de probabilidad**: Generar un nombre **fuerte** → `total_score` **entre 5 y 7** (propiedades entre **5 y 8**).
- **10% de probabilidad**: Generar un nombre **imponente y de máximo respeto** → `total_score` **entre 8 y 10** (propiedades entre **7 y 10**).

### **Reglas adicionales para asegurar la distribución correcta:**
1. **El nombre del vino debe reflejar su categoría**:  
   - Si es **débil**, debe sonar simple o sin prestigio.  
   - Si es **neutro**, debe sonar genérico pero aceptable.  
   - Si es **fuerte**, debe transmitir poder.  
   - Si es **imponente**, debe sonar exclusivo y legendario.  
2. **El `total_score` debe estar forzado dentro de su rango, sin excepciones.**  
3. **Los valores sensoriales deben estar dentro de los rangos adecuados al `total_score` para mantener coherencia.**  
4. **El precio debe reflejar la calidad del vino, siendo más alto para `total_score` elevados.**  

Sé altamente creativo en la generación del nombre y la descripción.
"""


            wine_generate = generate_text(prompt)
            print(wine_generate)
            clean_json_string = (
                wine_generate.replace("```json", "").replace("```", "").strip()
            )
            wine_data = json.loads(clean_json_string)
            self.fields["name"].initial = wine_data.get("name")
            self.fields["description"].initial = wine_data.get("description")
            self.fields["price"].initial = float(wine_data.get("price"))
            self.fields["category"].initial = wine_data.get("category")
            self.fields["body"].initial = wine_data.get("body")
            self.fields["aroma"].initial = wine_data.get("aroma")
            self.fields["taste"].initial = wine_data.get("taste")
            self.fields["tannins"].initial = wine_data.get("tannins")
            self.fields["acidity"].initial = wine_data.get("acidity")
            self.fields["sweetness"].initial = wine_data.get("sweetness")
            self.fields["aging"].initial = wine_data.get("aging")
