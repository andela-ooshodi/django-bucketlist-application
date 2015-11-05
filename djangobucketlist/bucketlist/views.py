"""
Views for bucketlist app
"""

from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login


from bucketlist.forms import LoginForm, RegistrationForm


class IndexView(TemplateView):
    template_name = 'bucketlist/index.html'

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
                    return redirect("/home")
            else:
                context = super(LoginView, self).get_context_data(**kwargs)
                context['loginform'] = form
                return render(request, self.template_name, context)
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
            return redirect("/home")
        else:
            context = super(RegistrationView, self).get_context_data(**kwargs)
            context['registrationform'] = form
            return render(request, self.template_name, context)


class HomeView(TemplateView):
    template_name = 'bucketlist/home.html'
