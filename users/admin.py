from django.contrib import admin
from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "coins", "victories")
    search_fields = ("user__username",)
    filter_horizontal = ("wines",)


admin.site.register(Profile, ProfileAdmin)
