from django.contrib import admin
from .models import Village, Remark, Resident

class RemarkInline(admin.TabularInline):
    model = Remark
    extra = 0
    max_num = 100
    show_change_link = True

class ResidentInline(admin.TabularInline):
    model = Resident
    extra = 0
    show_change_link = True

class RemarkAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields':['village','serial_no','days','types','user','charaset','character','character_img_url','date','text']})
    ]
    list_display = ['text', 'id', 'village', 'user_id', 'serial_no', 'days', 'types', 'user', 'character', 'charaset', 'character_img_url', 'date',]
    list_filter = ['village', 'user_id', 'days', 'types', 'user','charaset', 'character', 'date',]
    search_fields = ['text',]

class ResidentAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields':['village','resident','character','character_img_url','job','deathflag']})
    ]
    list_display = ['resident','village','character','character_img_url','job','deathflag','id',]

class VillageAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields':['name','auther','auther_name','charaset','charaset_name','character_img_url','created_date','started_date','updated_date','daytime_seconds','nighttime_seconds','days','nightflag','palflag','startflag','endflag','delflag']})
    ]
    inlines = [ResidentInline, RemarkInline]
    list_display = ['name','id','auther','auther_name','charaset','charaset_name','daytime_seconds','nighttime_seconds','days','nightflag','palflag','startflag','endflag','delflag','started_date','created_date','updated_date',]
    list_filter = ['created_date','started_date','updated_date','auther','auther_name','charaset','charaset_name','created_date','palflag','endflag','delflag',]
    search_fields = ['name','auther','auther_name',]

admin.site.register(Village, VillageAdmin)
admin.site.register(Remark, RemarkAdmin)
admin.site.register(Resident, ResidentAdmin)
