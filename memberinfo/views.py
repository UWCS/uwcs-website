from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import models
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.template import loader, Context, RequestContext

from random import choice
from string import *

from compsoc.memberinfo.models import *
from compsoc.memberinfo.forms import *
from compsoc.shortcuts import * 
from compsoc.settings import *

from datetime import datetime

from compsoc.recaptcha.client import captcha

'''
The following views are all related to the member profile section of the website.
'''

@login_required()
def index(request):

    # catch a DoesNotExist exception
    # and convert it to a value
    def failsafe(f,val):
        try: return f()
        except: return val

    # is there a non-fail reduce function
    def getQuota(st): 
       return reduce(lambda acc,q:acc+q.quantity,u.quota_set.filter(status=st),0)

    u = request.user
    shell = failsafe(lambda: u.shellaccount,False)
    db = failsafe(lambda: u.databaseaccount,False)

    try:
        name_form = NicknameForm(initial={'name': u.nicknamedetails.nickname})
    except NicknameDetails.DoesNotExist:
        name_form = NicknameForm()

    try:
        website = u.websitedetails
        website_form = WebsiteForm(initial={
            'url':website.websiteUrl,
            'title':website.websiteTitle,
        })
    except WebsiteDetails.DoesNotExist:
        website_form = WebsiteForm()

    try:
        gameids = u.gamingids
        gameid_form = GameidForm(initial={
            'steam':gameids.steamID,
            'xbox':gameids.xboxID,
            'psn':gameids.psnID,
            'xfire':gameids.xfireID,
        })
    except GamingIDs.DoesNotExist:
        gameid_form = GameidForm()

    my_lists = u.mailinglist_set.all()
    other_lists = []
    for list in MailingList.objects.all():
        if list not in my_lists:
            other_lists.append(list.list)

    return render_to_response('memberinfo/index.html',{
        'shell': shell,
        'shell_form':ShellForm(),
        'db': db,
        'db_form':DatabaseForm(),
        'quota': getQuota('PR'),
        'req_quota': getQuota('RE')*QUOTA_INC,
        'total_quota':getQuota('PR')*QUOTA_INC+BASE_QUOTA,
        'quota_form':QuotaForm(),
        'name_form':name_form,
        'website_form':website_form,
        'publish_form': PublishForm(initial={'publish':u.member.showDetails}),
        'gameid_form':gameid_form,
        'my_lists':my_lists,
        'other_lists':other_lists,
    },context_instance=RequestContext(request,{},[path_processor]))

@login_required()
def shell(request):
    return do_service(request,ShellForm,ShellAccount, 'shell',
        lambda acc: "You already own a shell account called %s" % acc.name)

@login_required()
def database(request):
    return do_service(request,DatabaseForm,DatabaseAccount, 'database',
        lambda acc: "You already own a database account called %s" % acc.name)

def do_service(request,form,klass,name,error):
    f = form(request.POST)
    if f.is_valid():
        n = f.cleaned_data['name']
        u = request.user

        try:
            acc = klass.objects.get(user=u)
            return render_to_response('memberinfo/request_error.html',{
                'name':name,
                'error':error(acc),
            },context_instance=RequestContext(request,{},[path_processor]))
        except klass.DoesNotExist:
            obj = klass(user=u,name=n,status='RE')
            obj.save()

            template_mail(
                'New service request',
                'memberinfo/service_techteam.html',
                {'realname':("%s %s"%(u.first_name,u.last_name)),'username':n,'what':name},
                COMPSOC_TECHTEAM_EMAIL,
                [COMPSOC_TECHTEAM_EMAIL])
        return HttpResponseRedirect('/member/')
    else:
        return render_to_response('memberinfo/form_errors.html',{
            'name':name,
            'all_errors':f.errors.items(),
        },context_instance=RequestContext(request,{},[path_processor]))

@login_required()
def quota(request):
    form = QuotaForm(request.POST)
    user = request.user
    if form.is_valid():
        amount = form.cleaned_data['quota']
        try:
            acc_name = user.shellaccount.name
            q = Quota.objects.create(user=user,quantity=amount,status='RE',date=datetime.now())
            template_mail(
                'Quota request',
                'memberinfo/quota_techteam',
                {'realname':user.member.all_name(),'username':acc_name,'amount':amount},
                user.email,
                [COMPSOC_TECHTEAM_EMAIL,COMPSOC_TREASURER_EMAIL])
            return HttpResponseRedirect('/member/')
        except ShellAccount.DoesNotExist:
            return render_to_response('memberinfo/request_error.html',{
                'name':'Quota',
                'error':'You don\'t have a shell account',
            },context_instance=RequestContext(request,{},[path_processor]))
    else:
        return render_to_response('memberinfo/request_error.html',{
            'name':'Quota',
            'error':"You must enter an integer as the amount",
        },context_instance=RequestContext(request,{},[path_processor]))

@login_required()
def lists(request):
    # update database
    user = request.user
    my_lists = request.user.mailinglist_set
    previous = set(my_lists.all())
    my_lists.clear()
    for mlist in MailingList.objects.all():
        if request.POST.has_key(mlist.list):
            my_lists.add(mlist)
    request.user.save()

    # update mailman
    now = set(my_lists.all())
    add,remove = now - previous,previous - now
    error = "Something else went wrong!"
    try:
        from compsoc.memberinfo.mailman import *
        try:
            for list in add: subscribe_member(user,list)
            for list in remove: unsubscribe_member(user,list)
            return HttpResponseRedirect('/member/')
        except MailmanError, e:
            error = e.msg
    except ImportError:
        if not DEBUG:
            error = "You don't have mailman installed and the site is running outside of DEBUG mode."
        else:
            error = ("If mailman had been installed we would have added %s and removed %s" % (str(add),str(remove)))
    return render_to_response('memberinfo/request_error.html',{
        'name':'Mailing Lists',
        'error':error,
    },context_instance=RequestContext(request,{},[path_processor]))

@login_required()
def set_nickname(request):
    u = request.user
    form = NicknameForm(request.POST)
    if form.is_valid():
        name = form.cleaned_data['name']
        try:
            nickname = u.nicknamedetails
            if name:
                nickname.nickname = name
                nickname.save()
            else:
                #empty nicks remove the nickname
                nickname.delete()
        except NicknameDetails.DoesNotExist:
            nickname = NicknameDetails.objects.create(user=u, nickname=name)
        return HttpResponseRedirect('/member/')
    else:
        return render_to_response('memberinfo/form_errors.html',{
            'name':'Nickname',
            'all_errors':form.errors.items(),
        },context_instance=RequestContext(request,{},[path_processor]))

@login_required()
def set_website(request):
    u = request.user
    form = WebsiteForm(request.POST)
    if form.is_valid():
        try:
            website = u.websitedetails
            website.websiteTitle = form.cleaned_data['title']
            website.websiteUrl = form.cleaned_data['url']
            website.save()
        except WebsiteDetails.DoesNotExist:
            WebsiteDetails.objects.create(user=u,websiteTitle=form.cleaned_data['title'],websiteUrl=form.cleaned_data['url'])
        return HttpResponseRedirect('/member/')
    else:
        return render_to_response('memberinfo/form_errors.html',{
            'name':'Website Details',
            'all_errors':form.errors.items(),
        },context_instance=RequestContext(request,{},[path_processor]))

@login_required()
def set_publish(request):
    u = request.user
    form = PublishForm(request.POST)
    if form.is_valid():
        member = u.member
        member.showDetails = form.cleaned_data['publish']
        member.save()
        return HttpResponseRedirect('/member/')
    else:
        return render_to_response('memberinfo/form_errors.html',{
            'name':'Publish Details',
            'all_errors':form.errors.items(),
        },context_instance=RequestContext(request,{},[path_processor]))

@login_required
def set_gameids(request):
    u = request.user
    form = GameidForm(request.POST)
    if form.is_valid():
        try: 
            gameids = u.gamingids
            gameids.steamID = form.cleaned_data['steam']
            gameids.xboxID = form.cleaned_data['xbox']
            gameids.psnID = form.cleaned_data['psn']
            gameids.xfireID = form.cleaned_data['xfire']
            gameids.save()
        except GamingIDs.DoesNotExist:
            GamingIDs.objects.create(user=u,steamID=form.cleaned_data['steam'],xboxID=form.cleaned_data['xbox'],psnID=form.cleaned_data['psn'],xfireID=form.cleaned_data['xfire'])
        return HttpResponseRedirect('/member/')
    else:
        return render_to_response('memberinfo/form_errors.html',{
            'name':'Gaming IDs',
            'all_errors':form.errors.items(),
        },context_instance=RequestContext(request,{},[path_processor]))

'''
End of Member Profile Section
'''
def member_list(request):
    users = []

    def get_website(user,f):
        try:
            return f(user.websitedetails)
        except WebsiteDetails.DoesNotExist:
            return False

    for user in User.objects.all():
        if user.member.showDetails and user.is_active:
            users.append((
                user.get_full_name(),
                user.member.get_nick(),
                get_website(user,lambda w: w.websiteTitle),
                get_website(user,lambda w: w.websiteUrl),
            ))
    
    return render_to_response('memberinfo/list.html',{
        'users': sorted(users,key=lambda (name,nick,title,url):name),
    },context_instance=RequestContext(request,{},[path_processor]))

def reset_password(request):
    try:
        # Do the password reset
        user_name = request.POST['user_name']
        user = User.objects.get(username__exact=user_name)
        password = User.objects.make_random_password()
        user.set_password(password)
        user.save()

        # Email the user
        template_mail(
            'Compsoc Password Reset',
            'memberinfo/reset_email',
            {'name':user_name,'password':password},
            WEBMASTER_EMAIL,
            [user.email])
        return render_to_response('memberinfo/password_reset_success.html',{
        },context_instance=RequestContext(request,{},[path_processor]))
    # If someone tries to reset the password of a user who doesn't exist, then report it
    except User.DoesNotExist:
        template_mail(
            'Warning: Failed Password Reset Attempt',
            'memberinfo/techteam_reset_email',
            {'name':user_name, 'ip':request.META['REMOTE_ADDR']},
            WEBMASTER_EMAIL,
            [WEBMASTER_EMAIL])
        return render_to_response('memberinfo/password_reset_no_name.html', {
            'tech':WEBMASTER_EMAIL,
        },context_instance=RequestContext(request,{},[path_processor]))

@login_required()
def reset_account(request,account):
    try:
        u = request.user
        name = (u.databaseaccount if account == 'db' else u.shellaccount).name
        type = 'Database' if account == 'db' else 'Shell'
        template_mail(
            'Password reset request',
            'memberinfo/account_techteam_email',
            {'name':u.get_full_name(),'type':type,'accname':name},
            u.email,
            [COMPSOC_TECHTEAM_EMAIL])
        return render_to_response('memberinfo/account_reset.html',{
        },context_instance=RequestContext(request,{},[path_processor]))
    except DatabaseAccount.DoesNotExist:
        error = "You don't have a database, so it can't be password reset"
    except ShellAccount.DoesNotExist:
        error = "You don't have a shell account, so it can't be password reset"
    return render_to_response('memberinfo/request_error.html',{
        'name':'Shell',
        'error':error,
    },context_instance=RequestContext(request,{},[path_processor]))
       
def create_guest(request):

    captcha_error = ""

    if request.method == 'POST':
        form = GuestForm(request.POST)
        
        captcha_response = captcha.submit(request.POST.get("recaptcha_challenge_field", None),
            request.POST.get("recaptcha_response_field", None),
            RECAPTCHA_PRIV_KEY, 
            request.META.get("REMOTE_ADDR", None)
        )
               
        if not captcha_response.is_valid:
            captcha_error = "&error=%s" % captcha_response.error_code
        elif form.is_valid():
            name = form.cleaned_data['username']
            u = form.save(commit=False)
            u.set_unusable_password()
            u.is_active = False
            u.save()
            Member.objects.create(user=u,guest=True,showDetails=False)
            NicknameDetails.objects.create(user=u,nickname=name)
            template_mail(
                'Guest account request',
                'memberinfo/guest_request_email',
                {'name':name},
                COMPSOC_EXEC_EMAIL,
                [u.email])
            template_mail(
                'Guest account request',
                'memberinfo/exec_guest_request_email',
                {'name':name},
                COMPSOC_EXEC_EMAIL,
                [COMPSOC_EXEC_EMAIL])

            return render_to_response('memberinfo/guest_request.html')
    else:
        form = GuestForm()
        
    return render_to_response('memberinfo/guest_form.html', {
        'form': form,
        'captcha_errpr':captcha_error,
#        'captcha':captcha.displayhtml(RECAPTCHA_PUB_KEY),
        'public_key':RECAPTCHA_PUB_KEY,
    })

def profiles(request,userid):
    try:
	u = User.objects.get(id__exact=userid)
        try:
	    gameids = u.gamingids
	    profile = {
		'name': u.get_full_name(),
		'steamid': gameids.steamID,
		'xboxid': gameids.xboxID,
		'psnid': gameids.psnID,
		'xfireid': gameids.xfireID,
	    }
	except GamingIDs.DoesNotExist:
	    profile = {'name': u.get_full_name(),}
	
	try:
	    profile['nickname'] = u.nicknamedetails.nickname
	except NicknameDetails.DoesNotExist:
	    profile['nickname'] = ""

	try:
	    profile['website_url'] = u.websitedetails.websiteUrl
	    profile['website_name'] = u.websitedetails.websiteTitle
	except WebsiteDetails.DoesNotExist:
	    pass	    

	return render_to_response('memberinfo/profile.html',
            profile,
	context_instance=RequestContext(request,{},[path_processor]))
    except User.DoesNotExist:
	error = "this user does not exist."
    return render_to_response('memberinfo/request_error.html',{
	        'name':'profile',
		'error':error,
	},context_instance=RequestContext(request,{},[path_processor]))
