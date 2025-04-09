from django.contrib import admin
from .models import Services,Category

# Register your models here.
@admin.register(Services)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'duration', 'time_slot']
    list_editable=['duration']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=['name', 'description']