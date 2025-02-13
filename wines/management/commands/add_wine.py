from django.core.management.base import BaseCommand
from wines.models import Wine, Category


class Command(BaseCommand):
    help = "Agrega un vino automáticamente"

    def handle(self, *args, **kwargs):
        # Crea un vino de ejemplo
        category = (
            Category.objects.first()
        )  # Toma la primera categoría si no tienes una específica
        wine = Wine.objects.create(
            name="Vino Ejemplo",
            description="Este es un vino de ejemplo.",
            price=25.99,
            category=category,
            body=2,
            aroma=2,
            taste=2,
            tannins=2,
            acidity=2,
            sweetness=2,
            aging=2,
        )

        self.stdout.write(
            self.style.SUCCESS(f"Vino '{wine.name}' agregado exitosamente.")
        )
