from django import forms
from django.contrib.auth.models import User

class DatabaseForm(forms.Form):
    name = forms.CharField()

class ShellForm(forms.Form):
    name = forms.CharField()

class QuotaForm(forms.Form):
    quota = forms.IntegerField(label='Units (x1000MB) quota:')

class NicknameForm(forms.Form):
    name = forms.CharField(required=False)

class WebsiteForm(forms.Form):
    url = forms.URLField()
    title = forms.CharField()

class PublishForm(forms.Form):
    publish = forms.BooleanField(label='Publish Details',required=False)

class GuestForm(forms.ModelForm):
    # enforce fields otherwise optional
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=75)
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email')
    
