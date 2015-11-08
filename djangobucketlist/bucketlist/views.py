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
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from bucketlist.models import BucketList, BucketlistItem
from bucketlist.forms_authentication import LoginForm, RegistrationForm
from bucketlist.forms_buckets import BucketListForm, BucketlistItemForm
import json
from datetime import datetime


class IndexView(TemplateView):
    template_name = 'bucketlist/index.html'

    def dispatch(self, request, *args, **kwargs):
        # redirect a user if already authenticated
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


class LoginRequiredMixin(object):
    # View mixin which requires that the user is authenticated.
    @method_decorator(login_required(login_url='/'))
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(
            request, *args, **kwargs)


class PaginationMixin(object):
    # grabs the page number in a get query string
    def dispatch(self, request, *args, **kwargs):
        self.page = request.GET.get('page')
        return super(PaginationMixin, self).dispatch(request, *args, **kwargs)


class BucketListView(LoginRequiredMixin, PaginationMixin, TemplateView):
    template_name = 'bucketlist/bucketlist.html'
    form_class = BucketListForm

    def get_context_data(self, **kwargs):
        buckets_all = BucketList.objects.filter(
            author_id=self.request.user.id).order_by('-date_modified')
        # limit the number of buckets per page to 10
        paginator = Paginator(buckets_all, 10)
        try:
            buckets = paginator.page(self.page)
        except PageNotAnInteger:
            # If page is not an integer, deliver the first page.
            buckets = paginator.page(1)
        except EmptyPage:
            # If page is out of range, deliver the last page
            buckets = paginator.page(paginator.num_pages)

        # get context
        context = super(BucketListView, self).get_context_data(**kwargs)
        username = kwargs['username']
        context['username'] = username
        context['bucketlistform'] = BucketListForm()
        context['buckets'] = buckets
        if username != self.request.user.username:
            # returns error if trying to access bucketlist not owned
            self.template_name = 'bucketlist/errors.html'

        return context

    def post(self, request, **kwargs):
        try:
            form = self.form_class(request.POST)
            bucketlist = form.save(commit=False)
            bucketlist.author = self.request.user
            bucketlist.save()
            return redirect('/bucketlist/{}/bucketitem'.format(bucketlist.id))
        except ValueError:
            # redirects to error page on adding an empty bucketlist
            return render(request, 'bucketlist/errors.html')

    def delete(self, request, **kwargs):
        bucketlist = BucketList.objects.get(
            pk=int(request.body.split('=')[1]))
        bucketitems = BucketlistItem.objects.filter(
            bucketlist_id=bucketlist.pk)

        bucketlist.delete()
        bucketitems.delete()

        return HttpResponse(
            json.dumps({'msg': 'success'}),
            content_type="application/json"
        )


class BucketItemView(LoginRequiredMixin, PaginationMixin, TemplateView):
    template_name = 'bucketlist/bucketitem.html'
    form_class = BucketlistItemForm

    def get_context_data(self, **kwargs):
        try:
            bucketitems_all = BucketlistItem.objects.filter(
                bucketlist_id=kwargs['bucketlistid']).order_by(
                'done', '-date_modified',
            )
            # limit the number of bucketitems per page to 10
            paginator = Paginator(bucketitems_all, 10)
            try:
                bucketitems = paginator.page(self.page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                bucketitems = paginator.page(1)
            except EmptyPage:
                # If page is out of range, deliver last page
                bucketitems = paginator.page(paginator.num_pages)

            # get context
            context = super(BucketItemView, self).get_context_data(**kwargs)
            # get the name of the bucketlist and check if it belongs to logged
            # in user
            context['name'] = BucketList.objects.filter(
                id=kwargs['bucketlistid'],
                author_id=self.request.user.id)[0].name
            context['bucketitems'] = bucketitems
            context['bucketitemform'] = BucketlistItemForm()
            context['bucketlistid'] = kwargs['bucketlistid']
        except IndexError:
            # returns error if trying to access bucketitems not owned
            self.template_name = 'bucketlist/errors.html'

        return context

    def post(self, request, **kwargs):
        bucketitem_name = request.POST.get('name')
        bucketitem = BucketlistItem(
            name=bucketitem_name,
            bucketlist=BucketList.objects.get(
                pk=kwargs['bucketlistid']))

        bucketitem.save()

        return HttpResponse(
            json.dumps({'msg': 'success'}),
            content_type="application/json"
        )

    def put(self, request, **kwargs):
        bucketitem = BucketlistItem.objects.get(
            pk=int(request.body.split('=')[1]))

        bucketitem.done = False if bucketitem.done else True
        bucketitem.date_modified = datetime.now
        bucketitem.save()

        return HttpResponse(
            json.dumps({'msg': 'success'}),
            content_type="application/json"
        )

    def delete(self, request, **kwargs):
        bucketitem = BucketlistItem.objects.get(
            pk=int(request.body.split('=')[1]))

        bucketitem.delete()

        return HttpResponse(
            json.dumps({'msg': 'success'}),
            content_type="application/json"
        )
