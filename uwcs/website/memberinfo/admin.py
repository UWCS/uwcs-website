from uwcs.website.memberinfo.models import *
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin,UserChangeForm,UserCreationForm
from django.utils.translation import ugettext, ugettext_lazy as _
from django.forms import widgets,ModelChoiceField
from forms import UserModelChoiceField

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
    """
    Customised user admin that includes the inlines
    for optional data such as website details or nickname
    """
    inlines = [
        MemberInline,
        NicknameDetailsInline,
        WebsiteDetailsInline,
        ShellAccountInline,
        DatabaseAccountInline,
        QuotaInline,
    ]
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active')

class SocietyChangeForm(UserChangeForm):
    """
    Form to modify the details of a Society object
    """
    representative = UserModelChoiceField()
    class Meta:
        model = Society

class SocietyCreationForm(UserCreationForm):
    """
    Form to create a new Society object
    """
    representative = UserModelChoiceField()
    class Meta:
        model = Society

class SocietyAdmin(UserAdmin):
    """
    Customised admin for a Society object. Includes the
    useful inlines for this model and extra field which
    represents the User acting as the current contact for this
    society
    """
    inlines = [
        WebsiteDetailsInline,
        ShellAccountInline,
        DatabaseAccountInline,
        QuotaInline,
    ]

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
