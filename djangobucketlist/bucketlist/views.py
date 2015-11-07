"""
Views for bucketlist app
"""

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from bucketlist.models import BucketList, BucketlistItem
from bucketlist.forms_authentication import LoginForm, RegistrationForm
from bucketlist.forms_buckets import BucketListForm, BucketlistItemForm
import json


class IndexView(TemplateView):
    template_name = 'bucketlist/index.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('/bucketlist/' + self.request.user.username)
        return super(IndexView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['loginform'] = LoginForm()
        context['registrationform'] = RegistrationForm()
        return context


class LoginView(IndexView):
    form_class = LoginForm

    def post(self, request, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/bucketlist/' + self.request.user.username)
            else:
                messages.add_message(
                    request, messages.ERROR, 'Incorrect username or password!')
                return redirect(
                    '/',
                    context_instance=RequestContext(request)
                )
        else:
            context = super(LoginView, self).get_context_data(**kwargs)
            context['loginform'] = form
            return render(request, self.template_name, context)


class RegistrationView(IndexView):
    form_class = RegistrationForm

    def post(self, request, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(username=request.POST['username'],
                                    password=request.POST['password'])
            login(request, new_user)
            return redirect("/bucketlist/" + self.request.user.username)
        else:
            context = super(RegistrationView, self).get_context_data(**kwargs)
            context['registrationform'] = form
            return render(request, self.template_name, context)


class PaginationMixin(object):

    def dispatch(self, request, *args, **kwargs):
        self.page = request.GET.get('page')
        return super(PaginationMixin, self).dispatch(request, *args, **kwargs)


class BucketListView(PaginationMixin, TemplateView):
    template_name = 'bucketlist/bucketlist.html'
    form_class = BucketListForm

    def get_context_data(self, **kwargs):
        buckets_list = BucketList.objects.filter(
            author_id=self.request.user.id).order_by('-date_modified')

        paginator = Paginator(buckets_list, 10)
        try:
            buckets = paginator.page(self.page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            buckets = paginator.page(1)
        except EmptyPage:
            # If page is out of range
            buckets = paginator.page(paginator.num_pages)

        # get context
        context = super(BucketListView, self).get_context_data(**kwargs)
        username = kwargs['username']
        context['username'] = username
        context['bucketlistform'] = BucketListForm()
        context['buckets'] = buckets
        if username != self.request.user.username:
            self.template_name = 'bucketlist/errors.html'

        return context

    def post(self, request, **kwargs):
        form = self.form_class(request.POST)
        bucketlist = form.save(commit=False)
        bucketlist.author = self.request.user
        bucketlist.save()
        return redirect('/bucketlist/{}/bucketitem'.format(bucketlist.id))


class BucketItemView(PaginationMixin, TemplateView):
    template_name = 'bucketlist/bucketitem.html'
    form_class = BucketlistItemForm

    def get_context_data(self, **kwargs):
        try:
            bucketitems_list = BucketlistItem.objects.filter(
                bucketlist_id=kwargs['bucketlistid'])
            paginator = Paginator(bucketitems_list, 10)
            try:
                bucketitems = paginator.page(self.page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                bucketitems = paginator.page(1)
            except EmptyPage:
                # If page is out of range
                bucketitems = paginator.page(paginator.num_pages)

            # get context
            context = super(BucketItemView, self).get_context_data(**kwargs)
            context['name'] = BucketList.objects.filter(
                id=kwargs['bucketlistid'],
                author_id=self.request.user.id)[0].name
            context['bucketitems'] = bucketitems
            context['bucketitemform'] = BucketlistItemForm()
            context['bucketlistid'] = kwargs['bucketlistid']
        except IndexError:
            self.template_name = 'bucketlist/errors.html'

        return context

    def post(self, request, **kwargs):
        post_name = request.POST.get('the_post')
        response_data = {}
        bucketitem = BucketlistItem(
            name=post_name,
            bucketlist=BucketList.objects.get(
                pk=kwargs['bucketlistid']))

        bucketitem.save()
        response_data['name'] = bucketitem.name
        response_data['bucketlist'] = bucketitem.bucketlist_id
        response_data['bucketpk'] = bucketitem.pk
        response_data['done'] = bucketitem.done

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
