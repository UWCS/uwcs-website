from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django import forms
from django.core.mail import send_mail
from compsoc.settings import COMPSOC_EXEC_EMAIL
from compsoc.events.models import *
from django.contrib.admin.views.decorators import staff_member_required

class EmailForm(forms.Form):
    subject = forms.CharField(max_length=30)
    message = forms.CharField()

@staff_member_required
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

class LocationForm(forms.Form):
    location = forms.ModelChoiceField(queryset=Location.objects.all())
    delete = forms.BooleanField(required=False)

@staff_member_required
def unify(request,location_id):
    '''
        Unifies location 'from_loc' (selected by user) with 'loc'
            * all events held at 'from_loc' are held at 'loc'
            * all seating rooms related to 'from_loc' are related to 'loc'
            * optionally deletes 'from_loc'
    '''
    loc = Location.objects.get(pk=location_id)
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            from_loc = form.cleaned_data['location']
            # move events and rooms
            from_loc.event_set.update(location=loc)
            from_loc.seatingroom_set.update(room=loc)
            if form.cleaned_data['delete']:
                from_loc.delete()
    else:
        form = LocationForm()

    return render_to_response('events/admin/unify_locations.html',{
        'location_id':location_id,
        'form': form,
        'title': "Unify Location %s" % loc.name,
        'location': loc.name,
        'user': request.user,
    })

