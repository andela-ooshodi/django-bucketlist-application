"""
view logic for performing CRUD operations on the bucketlist app
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, View
from django.contrib import messages
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from bucketlist.models import BucketList, BucketlistItem
from bucketlist.forms.form_buckets import BucketListForm, BucketlistItemForm
from datetime import datetime


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

    """
    view for listing and creating new bucketlists
    """

    template_name = 'bucketlist/bucketlist.html'
    form_class = BucketListForm

    def get_context_data(self, **kwargs):
        buckets_all = BucketList.objects.filter(
            author_id=self.request.user.id)
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
        context['username'] = self.request.user.username
        context['bucketlistform'] = BucketListForm()
        context['bucketitemform'] = BucketlistItemForm()
        context['buckets'] = buckets

        return context

    def post(self, request, **kwargs):
        try:
            form = self.form_class(request.POST)
            bucketlist = form.save(commit=False)
            bucketlist.author = self.request.user
            bucketlist.save()
            messages.success(
                request, 'New bucket successfully created!')
            return redirect(
                '/bucketlist',
                context_instance=RequestContext(request)
            )
        except ValueError:
            messages.error(
                request,
                'You attempted to enter an unnamed bucketlist')
            # redirects to error page on adding an empty bucketlist
            return render(request, 'bucketlist/errors.html')


class BucketListEditView(LoginRequiredMixin, View):

    """
    View for changing a bucketlist name
    """

    def post(self, request, **kwargs):
        bucketlist = BucketList.objects.filter(
            pk=kwargs['bucketlistid'], author_id=self.request.user).first()
        bucketlist.name = request.POST['name']
        if not bucketlist.name:
            messages.error(
                request,
                'You attempted to change to an empty name!')
            # redirects to error page on adding an empty name
            return render(request, 'bucketlist/errors.html')
        bucketlist.save()
        messages.success(
            request, 'Name change successful!')
        return redirect(
            '/bucketlist',
            context_instance=RequestContext(request)
        )


class BucketListDeleteView(LoginRequiredMixin, View):

    """
    view for deleting a bucketlist
    """

    def get(self, request, **kwargs):
        bucketlist = BucketList.objects.filter(
            pk=kwargs['bucketlistid'], author_id=self.request.user).first()
        if not bucketlist:
            messages.error(
                request, 'Unauthorized Access!')
            return render(request, 'bucketlist/errors.html')
        bucketlist.delete()
        messages.warning(
            request, 'Bucketlist Deleted!')
        return redirect(
            '/bucketlist',
            context_instance=RequestContext(request)
        )


class BucketItemView(LoginRequiredMixin, TemplateView):

    """
    view for creating bucketitems
    """

    def post(self, request, **kwargs):
        bucketitem_name = request.POST.get('name')
        if not bucketitem_name:
            messages.error(
                request,
                'You attempted to enter an unnamed bucketitem')
            # returns error if trying to add an empty item
            return render(request, 'bucketlist/errors.html')

        bucketitem = BucketlistItem(
            name=bucketitem_name,
            bucketlist=BucketList.objects.get(
                pk=kwargs['bucketlistid']))

        bucketitem.save()

        messages.success(
            request, 'Successfully added an item!')
        return redirect(
            '/bucketlist',
            context_instance=RequestContext(request)
        )


class BucketItemEditView(LoginRequiredMixin, View):

    """
    view for editing a bucketitem
    """

    def get(self, request, **kwargs):
        bucketitem = get_object_or_404(
            BucketlistItem,
            pk=kwargs['bucketitemid'])

        # check if the bucketitem belongs to the requester
        bucketlist = BucketList.objects.get(pk=bucketitem.bucketlist_id)
        if bucketlist.author_id != self.request.user.id:
            messages.error(
                request, 'Unauthorized access')
            # returns error for unauthorized access
            return render(request, 'bucketlist/errors.html')

        bucketitem.done = False if bucketitem.done else True
        bucketitem.date_modified = datetime.now

        bucketitem.save()

        messages.success(
            request, 'Status change successful!')
        return redirect(
            '/bucketlist',
            context_instance=RequestContext(request)
        )

    def post(self, request, **kwargs):
        bucketitem = get_object_or_404(
            BucketlistItem,
            pk=kwargs['bucketitemid'])
        bucketitem.name = request.POST['name']

        if not bucketitem.name:
            messages.error(
                request,
                'You tried to change to an empty name!')
            # redirects to error page on adding an empty name
            return render(request, 'bucketlist/errors.html')

        bucketitem.save()

        messages.success(
            request, 'Name change successful!')
        return redirect(
            '/bucketlist',
            context_instance=RequestContext(request)
        )


class BucketItemDeleteView(LoginRequiredMixin, View):

    """
    view for deleteing a bucketitem
    """

    def get(self, request, **kwargs):
        bucketitem = get_object_or_404(
            BucketlistItem,
            pk=kwargs['bucketitemid'])

        # check if the bucketitem belongs to the requester
        bucketlist = BucketList.objects.get(pk=bucketitem.bucketlist_id)
        if bucketlist.author_id != self.request.user.id:
            messages.error(
                request,
                'Unauthorized access')
            # returns error for unauthorized access
            return render(request, 'bucketlist/errors.html')

        bucketitem.delete()

        messages.warning(
            request, 'Item Deleted!')
        return redirect(
            '/bucketlist',
            context_instance=RequestContext(request)
        )
