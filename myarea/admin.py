from django.contrib import admin
from .models import Profile, Neighbourhood, Post, Business, Join

# Register your models here.
admin.site.register(Profile)
admin.site.register(Neighbourhood)
admin.site.register(Post)
admin.site.register(Business)
admin.site.register(Join)