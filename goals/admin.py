from django.contrib import admin

from goals.models import GoalCategory, Goal


class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created', 'updated')
    search_fields = ('title', 'user')


admin.site.register(GoalCategory, GoalCategoryAdmin)


class GoalAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'priority', 'created', 'updated')
    search_fields = ('title', 'desc', 'user')


admin.site.register(Goal, GoalAdmin)
