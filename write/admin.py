from django.contrib import admin
from .models import HeartUser
# Register your models here.
class HeartUserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email")
    search_fields = ("username", "email")

admin.site.register(HeartUser, HeartUserAdmin)