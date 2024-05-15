from django.contrib import admin
from .models import FoodItem, Cart


class FoodItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'serving', 'calories', 'food_type', 'image')
    list_filter = ('food_type',)
    search_fields = ('name', 'calories')


admin.site.register(FoodItem, FoodItemAdmin)
admin.site.register(Cart)
