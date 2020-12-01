from django.contrib import admin

from .models import *

class CategoryAdmin(admin.ModelAdmin):
    fields = ['title']


admin.site.register(Category, CategoryAdmin),
admin.site.register(Product)
