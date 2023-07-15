from django.contrib import admin

from record.models import Balance, From, Record, To

admin.site.register(Balance, admin.ModelAdmin)
admin.site.register(From, admin.ModelAdmin)
admin.site.register(Record, admin.ModelAdmin)
admin.site.register(To, admin.ModelAdmin)
