from django import forms

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
    
