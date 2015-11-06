"""
Views for bucketlist app
"""

from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.template import RequestContext

from bucketlist.models import BucketList, BucketlistItem
from bucketlist.forms_authentication import LoginForm, RegistrationForm
from bucketlist.forms_buckets import BucketListForm, BucketlistItemForm


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


class BucketListView(TemplateView):
    template_name = 'bucketlist/bucketlist.html'
    form_class = BucketListForm

    def get_context_data(self, **kwargs):
        context = super(BucketListView, self).get_context_data(**kwargs)
        username = kwargs['username']
        context['username'] = username
        context['bucketlistform'] = BucketListForm()
        context['buckets'] = BucketList.objects.filter(
            author_id=self.request.user.id).order_by('-date_modified')

        if username != self.request.user.username:
            self.template_name = 'bucketlist/errors.html'

        return context

    def post(self, request, **kwargs):
        form = self.form_class(request.POST)
        bucketlist = form.save(commit=False)
        bucketlist.author = self.request.user
        bucketlist.save()
        return redirect('/bucketlist/{}/bucketitem'.format(bucketlist.id))


class BucketItemView(TemplateView):
    template_name = 'bucketlist/bucketitem.html'
    form_class = BucketlistItemForm

    def get_context_data(self, **kwargs):
        try:
            context = super(BucketItemView, self).get_context_data(**kwargs)
            context['name'] = BucketList.objects.filter(
                id=kwargs['bucketlistid'],
                author_id=self.request.user.id)[0].name
            context['bucketitems'] = BucketlistItem.objects.filter(
                bucketlist_id=kwargs['bucketlistid'])
            context['bucketitemform'] = BucketlistItemForm()
        except IndexError:
            self.template_name = 'bucketlist/errors.html'

        return context

    def post(self, request, **kwargs):
        pass
