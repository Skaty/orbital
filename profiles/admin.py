from django.contrib import admin

# Register your models here.
from profiles.models import Preferences


@admin.register(Preferences)
class PreferencesModelAdmin(admin.ModelAdmin):
    model = Preferences