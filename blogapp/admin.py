from django.contrib import admin
from blogapp.models import Blogpost,Comments
# Register your models here.
admin.site.register((Blogpost,Comments))