from django.contrib import admin

from .forms import WineAdminForm
from .models import Category, Wine


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    list_filter = ("name",)

    def view_category(self, request, queryset):
        for category in queryset:
            self.message_user(request, f"Category: {category.name}!")

    view_category.short_description = "Ver categorías seleccionadas"

    actions = [view_category]


class WineAdmin(admin.ModelAdmin):

    def view_total_score(self, request, queryset):
        for wine in queryset:
            self.message_user(request, f"{wine.name} tiene de poder {wine.total_score()} unidades!")

    view_total_score.short_description = "Ver el poder de los vinos seleccionados"

    actions = [view_total_score]
    form = WineAdminForm


admin.site.register(Wine, WineAdmin)
