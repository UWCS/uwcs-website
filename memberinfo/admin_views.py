from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from compsoc.memberinfo.models import *
from compsoc.shortcuts import template_mail, path_processor
from compsoc.settings import COMPSOC_EXEC_EMAIL,COMPSOC_TECHTEAM_EMAIL

@user_passes_test(lambda u: u.is_staff)
def guest_list(request):
    return render_to_response('admin/memberinfo/member/guests.html', {
        'guests':filter(lambda u: u.member.guest and not u.is_active,User.objects.all()),
    },context_instance=RequestContext(request,{},[path_processor]))

@user_passes_test(lambda u: u.is_staff)
def account_list(request):
    return render_to_response('admin/memberinfo/member/accounts.html', {
        'shell_requests': ShellAccount.objects.filter(status='RE'),
        'database_requests': DatabaseAccount.objects.filter(status='RE'),
    },context_instance=RequestContext(request,{},[path_processor]))

@user_passes_test(lambda u: u.is_staff)
def accept_guest(request,user_id):
    u = User.objects.get(id=user_id)
    u.is_active = True
    pwd = User.objects.make_random_password()
    u.set_password(pwd)
    u.save()
    template_mail(
        'Guest account Acceptance',
        'admin/memberinfo/guest_accept_email',
        {'name':u.username,'password':pwd},
        COMPSOC_EXEC_EMAIL,
        [u.email])
    return HttpResponseRedirect('/admin/memberinfo/guests/')

@user_passes_test(lambda u: u.is_staff)
def reject_guest(request,user_id):
    u = User.objects.get(id=user_id)
    name = u.username
    email = u.email
    
    u.member.delete()
    u.nicknamedetails.delete()
    u.delete()
    
    template_mail(
        'Guest account Rejection',
        'admin/memberinfo/guest_reject_email',
        {'name':name},
        COMPSOC_EXEC_EMAIL,
        [email])

    return HttpResponseRedirect('/admin/memberinfo/guests/')
    
