from django.contrib import admin

from .models import Question, Choice

# class to Choice
class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 3

# this class must be inherited from ModelAdmin
class QuestionAdmin(admin.ModelAdmin):

    list_display = ["question_text", "pub_date", "was_published_recently"]
    list_filter = ["pub_date"]
    search_fields = ["question_text"]
    # using fieldset to group fields
    # first fieldset name is None
    # second fieldset name is DateInformation
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date Information", {"fields": ["pub_date"]})
    ]
    inlines = [ChoiceInLine]

# Register your models here.
admin.site.register(Question, QuestionAdmin)
