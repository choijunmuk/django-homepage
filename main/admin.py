from django.contrib import admin
from .models import Question, Photo

class PhotoInline(admin.TabularInline):
    model = Photo

class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['subject']
    inlines = [PhotoInline, ]

admin.site.register(Question, QuestionAdmin)

# Register your models here.
