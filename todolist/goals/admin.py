from django.contrib import admin

from todolist.goals.models import GoalCategory, Goal, GoalComment, Board, BoardParticipant


@admin.register(GoalCategory)
class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created", "updated")
    search_fields = ("title", "user")


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created", "updated")
    search_fields = ("title", "description")


@admin.register(GoalComment)
class GoalCommentsAdmin(admin.ModelAdmin):
    list_display = ("text", "created", "updated")
    search_fields = ("text",)


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ("title", "created", "updated")
    search_fields = ("title",)


@admin.register(BoardParticipant)
class BoardParticipantAdmin(admin.ModelAdmin):
    list_display = ("user", "created", "updated")
    search_fields = ("user",)
