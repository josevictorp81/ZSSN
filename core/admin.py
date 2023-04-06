from django.contrib import admin

from .models import Survivor, Resource

@admin.register(Survivor)
class SurvivorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'age', 'sex', 'infected']
    search_fields = ['name', 'sex', 'infected']
    list_display_links = ['id', 'name']
    list_per_page = 20


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'quantity', 'survivor']
    list_display_links = ['id', 'name']
    