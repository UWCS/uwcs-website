from django import forms
from django.contrib.auth.models import User
import re
pattern = re.compile(r'[^a-z0-9]')

class DatabaseForm(forms.Form):
    name = forms.CharField()
    def clean_name(self):
        name = self.cleaned_data['name']
        if re.search(pattern, name):
            raise forms.ValidationError("Please enter only lowercase characters and numbers")
        return name

class ShellForm(forms.Form):
    name = forms.CharField()
    def clean_name(self):
        name = self.cleaned_data['name']
        if re.search(pattern, name):
            raise forms.ValidationError("Please enter only lowercase characters and numbers")
        return name

class QuotaForm(forms.Form):
    quota = forms.IntegerField(label='Units (x1000MB) quota:')

class NicknameForm(forms.Form):
    name = forms.CharField(required=False)

class WebsiteForm(forms.Form):
    url = forms.URLField()
    title = forms.CharField()

class GameidForm(forms.Form):
    steam = forms.CharField(required=False)
    xbox = forms.CharField(required=False)
    psn = forms.CharField(required=False)
    xfire = forms.CharField(required=False)

class PublishForm(forms.Form):
    publish = forms.BooleanField(label='Publish Details',required=False)

class GuestForm(forms.ModelForm):
    # enforce fields otherwise optional
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=75)
    reason = forms.CharField(
        label='Relation to society',
        widget=forms.Textarea,
    )
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email')

class UserModelChoiceField(forms.ModelChoiceField):
    '''
    Uses a formatted name as the label for selecting a user

    {nick} ({full name})
    or
    {full name}

    also sorts by nick, then full name
    '''
    def __init__(self, *args, **kwargs):
        if not kwargs.has_key('queryset'):
            kwargs['queryset'] = User.objects.all()

        kwargs['queryset'] = kwargs['queryset'].select_related('nicknamedetails').order_by('nicknamedetails__nickname','first_name','last_name')
        super(UserModelChoiceField, self).__init__(*args, **kwargs)

    def label_from_instance(self, obj):
        return obj.nicknamedetails and "%s (%s)" % (obj.nicknamedetails.nickname, obj.get_full_name()) or obj.get_full_name()
