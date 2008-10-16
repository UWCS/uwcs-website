from Compsoc.memberinfo.models import *
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.db import models
from django.http import HttpResponseRedirect

@login_required()
def index(request):

    # catch a DoesNotExist exception
    # and convert it to a falsehood
    def failsafe(f,val):
        try: return f()
        except: return val

    # is there a non-fail reduce function
    def getQuota(st): 
       return reduce(lambda acc,q:acc+q.quantity,u.quota_set.filter(status=st),0)

    u = request.user
    shell = failsafe(lambda: u.shellaccount,False)
    db = failsafe(lambda: u.databaseaccount,False)
    name = failsafe(lambda: u.nicknamedetails,"")
    website = failsafe(lambda: u.websitedetails,False)
    pub = failsafe(lambda: u.member.showDetails,False)

    (quota,req_quota) = (getQuota('PR'),getQuota('RE'))

    my_lists = u.mailinglist_set.all()
    other_lists = []
    for list in MailingList.objects.all():
        if list not in my_lists:
            other_lists.append(list.list)

    dict = {
        'shell': shell,
        'db': db,
        'quota': quota,
        'req_quota': req_quota*500,
        'total_quota':quota*500+1000,
        'name':name.nickname,
        'url':website.websiteUrl if website else "",
        'title':website.websiteTitle if website else "",
        'my_lists':my_lists,
        'other_lists':other_lists,
        'publish_details': pub,
    }
    return render_to_response('memberinfo/index.html',dict)

@login_required()
def shell(request):
    n = request.POST['shell']
    u = request.user

    try:
        ShellAccount.objects.get(user=u)
    except:
    # TODO: sanity check name
        s = ShellAccount(user=u,name=n,status='RE')
        s.save()
    return HttpResponseRedirect('/member/')

@login_required()
def database(request):
    n = request.POST['db']
    u = request.user

    try:
        DatabaseAccount.objects.get(user=u)
    except:
    # TODO: sanity check name
        db = DatabaseAccount(user=u,name=n,status='RE')
        db.save()
    return HttpResponseRedirect('/member/')

@login_required()
def quota(request):
    amount = request.POST['quota']
    q = Quota(user=request.user,quantity=amount,status='RE')
    q.save()
    return HttpResponseRedirect('/member/')

@login_required()
def lists(request):
    my_lists = request.user.mailinglist_set
    my_lists.clear()
    for list in MailingList.objects.all():
        try:
            request.POST[list.list]
            my_lists.add(list)
        except: pass
    request.user.save()
    return HttpResponseRedirect('/member/')

@login_required()
def details(request):
    u = request.user
    name = request.POST['name']
    url = request.POST['url']
    title = request.POST['title']
    try: publish = request.POST['publish']
    except: publish = False

    try:
        member = u.member
        member.showDetails = publish
    except Member.DoesNotExist:
        member = Member(user=u,showDetails=publish)
    member.save()

    try:
        website = u.websitedetails
        website.websiteTitle = title
        website.websiteUrl = url
    except WebsiteDetails.DoesNotExist:
        website = WebsiteDetails(user=u,websiteTitle=title,websiteUrl=url)
    website.save()
    
    return HttpResponseRedirect('/member/')

def member_list(request):
    users = []

    def get_website(user,f):
        try:
            return f(user.websitedetails)
        except WebsiteDetails.DoesNotExist:
            return False

    for user in User.objects.all():
        try:
            if user.member.showDetails:
                users.append((
                    user.get_full_name(),
                    user.member.name(),
                    get_website(user,lambda w: w.websiteTitle),
                    get_website(user,lambda w: w.websiteUrl),
                ))
        # Don't need to display guest accounts
        except Member.DoesNotExist: pass
    
    dict = {
        'users': users
    }
    return render_to_response('memberinfo/list.html',dict)
