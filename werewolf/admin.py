from django.contrib import admin
from .models import Choice, Question, Village, Remark

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields':['question_text']}),('Date information', {'fields':['pub_date']}),]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']

class RemarkInline(admin.TabularInline):
    model = Remark
    extra = 1

class VillageAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields':['name']}),('Date information', {'fields':['created_date']}),]
    inlines = [RemarkInline]
    list_display = ('name','created_date')
    list_filter = ['created_date']
    search_fields = ['name']

admin.site.register(Question, QuestionAdmin)
admin.site.register(Village, VillageAdmin)
admin.site.register(Remark)
