from django.contrib import admin
from accounts.models import *


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id',  'name','get_user_email','get_school_name',)
    search_fields = ('name',)

    @admin.display(description='Email') 
    def get_user_email(self, obj):
        return obj.user.email
    
    @admin.display(description='School Name')
    def get_school_name(self, obj):
        return obj.school_name.name if obj.school_name else 'N/A'
    
admin.site.register(UserProfile,UserProfileAdmin)

class SchoolAdmin(admin.ModelAdmin):
    list_display = ('pk','name',)
    search_fields = ('name',)
    
admin.site.register(School,SchoolAdmin)