from Compsoc.cms.models import *
from django.contrib.admin.views.decorators import staff_member_required
from django import forms
from django.shortcuts import render_to_response,get_object_or_404
from datetime import datetime
from django.http import HttpResponseRedirect

class PageForm(forms.Form):
    slug = forms.CharField(max_length=100)
    title = forms.CharField(max_length=100)
    comment = forms.CharField(max_length=100)
    text = forms.CharField(widget=forms.Textarea)
    login = forms.BooleanField(required=False)

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
            
    elif page_id != None:
        page = get_object_or_404(Page,id=page_id)
        rev = page.get_data()
        data = {
            'slug':page.slug,
            'title':rev.title,
            'comment':rev.comment,
            'text':rev.text,
            'login':rev.login,
        }
        form = PageForm(data)
    else:
        form = PageForm()

    return render_to_response('cms/admin/addedit.html', {
        'form': form,
        'user': request.user,
        'id': page_id,
    })
