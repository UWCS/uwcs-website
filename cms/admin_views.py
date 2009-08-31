from compsoc.cms.models import *
from django.contrib.admin.views.decorators import staff_member_required
from django import forms
from django.shortcuts import *
from datetime import datetime
from django.http import HttpResponseRedirect
from django.forms.util import ErrorList
from django.template import RequestContext
from compsoc.shortcuts import path_processor

class PageForm(forms.Form):
    slug = forms.CharField(max_length=60)
    title = forms.CharField(max_length=60)
    comment = forms.CharField(max_length=30)
    text = forms.CharField(widget=forms.Textarea)
    login = forms.BooleanField(required=False)

    def clean_slug(self):
        slug = self.cleaned_data['slug']
        return slug.rstrip('/')
    
    def clean_comment(self):
        comment = self.cleaned_data['comment']
        if comment == 'Please type a comment':
            raise forms.ValidationError("Don't just enter the same comment, actually enter one")
        return comment


@staff_member_required
def revision(request,rev_id):
    rev = get_object_or_404(PageRevision,id=rev_id)
    if request.method == 'POST':
        # clone
        rev.id = None
        rev.date_written = datetime.now()
        rev.comment = request.POST['comment']
        rev.save()
        return HttpResponseRedirect('/admin/cms/page/'+str(rev.page.id))
        
    else: 
        return render_to_response('cms/admin/view_revision.html', {
            'revision':rev,
        },context_instance=RequestContext(request,{},[path_processor]))

@staff_member_required
def add_edit(request,page_id=None):
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            try:
                page = Page.objects.get(id=page_id)
                page.slug = form.cleaned_data['slug']
            except Page.DoesNotExist:
                page = Page(slug=form.cleaned_data['slug'])
            
            page.save()
            rev = PageRevision(page=page,
                title = form.cleaned_data['title'],
                text = form.cleaned_data['text'],
                comment = form.cleaned_data['comment'],
                login = form.cleaned_data['login'],
                date_written = datetime.now(),
            )
            rev.save()
            return HttpResponseRedirect('/admin/cms/page/'+str(page.id))
        else:
            comments = []
            page = None
    elif page_id != None:
        page = get_object_or_404(Page,id=page_id)
        rev = page.get_data()
        data = {
            'slug':page.slug,
            'title':rev.title,
            'comment':'Please type a comment',
            'text':rev.text,
            'login':rev.login,
        }
        form = PageForm(data)
        # remove the 'please type a comment' error on first binding
        form.errors['comment'] = ErrorList()
        comments = map(lambda rev: (rev.comment,rev.id),page.pagerevision_set.order_by('-date_written'))
    else:
        data = {
            'slug':request.GET.get('slug',""),
            'comment':'Please type a comment',
        }
        form = PageForm(data)

        # this apparently suppresses error messages we don't want to see this time
        form.errors['slug'] = ErrorList()
        form.errors['title'] = ErrorList()
        form.errors['comment'] = ErrorList()
        form.errors['text'] = ErrorList()
        comments = []
        page = None

    return render_to_response('cms/admin/addedit.html', {
        'form': form,
        'id': page_id,
        'comments':comments,
        'slug': page.slug if page else None,
    },context_instance=RequestContext(request,{},[path_processor]))

