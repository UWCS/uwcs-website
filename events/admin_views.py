from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django import forms
from django.core.mail import send_mail
from compsoc.settings import COMPSOC_EXEC_EMAIL
from compsoc.events.models import Event

class EmailForm(forms.Form):
    subject = forms.CharField(max_length=30)
    message = forms.CharField()

def email_signups(request,event_id):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            event = Event.objects.get(id=event_id)
            for signup in event.signup_set.all():
                signup.user.email_user(subject, message, COMPSOC_EXEC_EMAIL)
            return render_to_response('events/admin/email_signups_done.html',{'user':request.user})
    else:
        form = EmailForm()

    return render_to_response('events/admin/email_signups_form.html', {
        'form': form,
        'user': request.user,
    })    
    
