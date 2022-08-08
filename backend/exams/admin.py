from django.contrib import admin
from django.contrib.admin.sites import site
from .models import *

admin.site.register(ExamCohort)
admin.site.register(ExamQuestion)
admin.site.register(Choice)
admin.site.register(Vote)

# @admin.register(ExamCohort)
# class ExamCohortAdmin(admin.ModelAdmin):
#     search_fields = ('user', 'title', 'examID', 'is_published', )
#     list_editable = ('title', 'is_published',)
#     list_display = ('title', 'user', 'is_published', 'created_on')
#     list_filter = ('user', 'title', 'is_published', 'created_on')
#     fieldsets = (
#         (None, {'fields': ('user', 'title', 'examID',)}),
#         ('Members', {'fields': ('members',)}),
#         ('Visibility', {'fields': ('is_published',)}),
#     )