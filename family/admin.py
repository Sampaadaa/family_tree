from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Person, Relationship

admin.site.register(Person)
admin.site.register(Relationship)
