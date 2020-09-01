from django.contrib import admin

from .models import Category, Expense

admin.site.register(Category)
admin.site.register(Expense)
