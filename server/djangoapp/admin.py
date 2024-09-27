from django.contrib import admin
from .models import CarMake, CarModel

# Register your models here.


# Registering models with their respective admins
admin.site.register(CarMake)
admin.site.register(CarModel)
# CarModelInline class

# CarModelAdmin class
# djangoapp/admin.py
# @admin.register(CarMake)
# class CarMakeAdmin(admin.ModelAdmin):
#     list_display = ('name', 'description')

# @admin.register(CarModel)
# class CarModelAdmin(admin.ModelAdmin):
#     list_display = ('name', 'car_make', 'type', 'year')
#     list_filter = ('car_make', 'type', 'year')
#     search_fields = ('name',)

# CarMakeAdmin class with CarModelInline

# Register models here
