from django.contrib import admin

from .forms import WineAdminForm
from .models import Category, Wine


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    list_filter = ("name",)

    # Acción personalizada para saludar miembros
    def view_category(self, request, queryset):
        for category in queryset:
            self.message_user(request, f"Category: {category.name}!")

    view_category.short_description = "Ver categorías seleccionadas"

    actions = [view_category]


class WineAdmin(admin.ModelAdmin):
    form = WineAdminForm


admin.site.register(Wine, WineAdmin)
