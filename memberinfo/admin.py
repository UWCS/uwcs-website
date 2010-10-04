from compsoc.memberinfo.models import *
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin,UserChangeForm,UserCreationForm
from django.utils.translation import ugettext, ugettext_lazy as _

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

class SocietyChangeForm(UserChangeForm):
    class Meta:
        model = Society

class SocietyCreationForm(UserCreationForm):
    class Meta:
        model = Society

class SocietyAdmin(UserAdmin):
    def __init2__(self, *args, **kwargs):
        super(SocietyAdmin, self).__init__(*args,**kwargs)
        fields = list(SocietyAdmin.fieldsets[0][1]['fields'])
        fields.append('representative')
        SocietyAdmin.fieldsets[0][1]['fields'] = fields
    inlines = [MemberInline,
               NicknameDetailsInline,
               WebsiteDetailsInline,
               ShellAccountInline,
               DatabaseAccountInline,
               QuotaInline,]

    # these are used for the modify form
    fieldsets = (
        (None, {'fields': ('username', 'password', 'representative')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Groups'), {'fields': ('groups',)}),
    )

    # these are used for the creation form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'representative')}
        ),
    )

    # these are used in the index
    list_display = ('username', 'representative', 'email', 'first_name', 'last_name', 'is_active', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active')

    form = SocietyChangeForm
    add_form = SocietyCreationForm

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

admin.site.register(Society, SocietyAdmin)
