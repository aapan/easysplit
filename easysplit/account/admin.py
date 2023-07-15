from django.contrib import admin

from account.models import Group, Member

admin.site.register(Group, admin.ModelAdmin)
admin.site.register(Member, admin.ModelAdmin)
