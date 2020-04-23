from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Entry
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator

# Create your views here.
class HomeView(LoginRequiredMixin, ListView):
    model = Entry
    template_name = 'entries/index.html'
    context_object_name = "blog_entries"
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        following_list = user.userprofile.following.all()
        blog_entries = []
        for i in following_list:
            blog_entries += Entry.objects.order_by('entry_date').filter(entry_author = i.following.user)
        blog_entries +=  Entry.objects.order_by('entry_date').filter(entry_author = user)
        blog_entries.reverse()
        return blog_entries


class EntryView(LoginRequiredMixin, DetailView):
    model = Entry
    template_name = 'entries/entry_detail.html'
    context_object_name = "entry"


class CreateEntryView(LoginRequiredMixin, CreateView):
    model = Entry
    template_name = 'entries/create_entry.html'
    fields = ['entry_title', 'entry_text']

    def form_valid(self, form):
        form.instance.entry_author = self.request.user
        return super().form_valid(form)
