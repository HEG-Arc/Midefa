# Core Django imports
from django.contrib import admin

# Third-party app imports

# Gelato imports
from .models import Project, Sprint, TrelloBoard, TrelloList, TrelloCard, TrelloCheckList, TrelloCheckListItem, TrelloMember


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    pass


@admin.register(Sprint)
class SprintAdmin(admin.ModelAdmin):
    pass


@admin.register(TrelloBoard)
class TrelloBoardAdmin(admin.ModelAdmin):
    pass


@admin.register(TrelloList)
class TrelloListAdmin(admin.ModelAdmin):
    pass


@admin.register(TrelloCard)
class TrelloCardAdmin(admin.ModelAdmin):
    pass


@admin.register(TrelloCheckList)
class TrelloCheckListAdmin(admin.ModelAdmin):
    pass


@admin.register(TrelloCheckListItem)
class TrelloCheckListItemAdmin(admin.ModelAdmin):
    pass


@admin.register(TrelloMember)
class TrelloMemberAdmin(admin.ModelAdmin):
    pass
