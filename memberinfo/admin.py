from compsoc.memberinfo.models import *
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

class MemberJoinAdmin(admin.ModelAdmin):
    list_filter = ['year']

class MemberInline(admin.StackedInline):
    model = Member

class WebsiteDetailsInline(admin.StackedInline):
    model = WebsiteDetails

class NicknameDetailsInline(admin.StackedInline):
    model = NicknameDetails

class ShellAccountInline(admin.StackedInline):
    model = ShellAccount

class DatabaseAccountInline(admin.StackedInline):
    model = DatabaseAccount

class QuotaInline(admin.TabularInline):
    model = Quota

class MyUserAdmin(UserAdmin):
    inlines = [MemberInline,
               NicknameDetailsInline,
               WebsiteDetailsInline,
               ShellAccountInline,
               DatabaseAccountInline,
               QuotaInline,]
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active')

# re-register useradmin
admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)

#admin.site.register(Member)
#admin.site.register(WebsiteDetails)
#admin.site.register(NicknameDetails)
admin.site.register(MemberJoin,MemberJoinAdmin)
#admin.site.register(ShellAccount)
#admin.site.register(DatabaseAccount)
#admin.site.register(Quota)
admin.site.register(MailingList)
admin.site.register(Term)
admin.site.register(ExecPosition)
admin.site.register(ExecPlacement)
