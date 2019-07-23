from django.contrib import admin

# Register your models here.
from Blogapp.models import *

admin.site.register(Blog)
admin.site.register(Author)
admin.site.register(Type)