from Compsoc.memberinfo.models import *
from django.contrib import admin

class MemberJoinAdmin(admin.ModelAdmin):
    list_filter = ['year']

admin.site.register(Member)
admin.site.register(WebsiteDetails)
admin.site.register(NicknameDetails)
admin.site.register(MemberJoin,MemberJoinAdmin)
admin.site.register(ShellAccount)
admin.site.register(DatabaseAccount)
admin.site.register(Quota)
admin.site.register(MailingList)
admin.site.register(Term)

