# Core Django imports
from django.contrib import admin

# Third-party app imports

# Gelato imports
from .models import Sprint


@admin.register(Sprint)
class SprintAdmin(admin.ModelAdmin):
    pass
