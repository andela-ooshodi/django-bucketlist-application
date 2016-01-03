"""
View logic for authentication for the bucketlist app
"""
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.template import RequestContext
from bucketlist.forms.form_authentication import LoginForm, RegistrationForm


class IndexView(TemplateView):
    template_name = 'bucketlist/index.html'

    def dispatch(self, request, *args, **kwargs):
        # redirect a user if already authenticated
        if request.user.is_authenticated():
            return redirect('/bucketlist')
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
                    messages.success(
                        request, 'Welcome Back!!')
                    return redirect(
                        '/bucketlist',
                        context_instance=RequestContext(request)
                    )
            else:
                messages.error(
                    request, 'Incorrect username or password!')
                return redirect(
                    '/login',
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
            new_user = authenticate(
                username=request.POST['username'],
                password=request.POST['password'])
            login(request, new_user)
            messages.success(
                request, 'Registration successful!!')
            return redirect(
                '/bucketlist',
                context_instance=RequestContext(request)
            )
        else:
            messages.error(
                request, 'Error at registration!')
            return redirect(
                '/register',
                context_instance=RequestContext(request)
            )
