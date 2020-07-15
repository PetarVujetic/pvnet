from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Entry, Comment
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect



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
            blog_entries += Entry.objects.order_by('-entry_date').filter(entry_author = i.following.user)

        return blog_entries


class EntryView(LoginRequiredMixin, DetailView):
    model = Entry
    template_name = 'entries/entry_detail.html'
    context_object_name = "entry"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = Comment.objects.filter(comment_entry = context['entry'])
        context['comments'] = comments
        return context


class CreateEntryView(LoginRequiredMixin, CreateView):
    model = Entry
    template_name = 'entries/create_entry.html'
    fields = ['entry_title', 'entry_text']

    def form_valid(self, form):
        form.instance.entry_author = self.request.user
        return super().form_valid(form)

def createComment(request):
    comment_author = request.user
    comment_entry = get_object_or_404(Entry, pk = request.POST.get('pk'))
    comment_text = request.POST.get('comment_text')

    Comment.objects.create(comment_author=comment_author, comment_entry=comment_entry, comment_text = comment_text)
    comments = Comment.objects.filter(comment_entry=comment_entry)
    print(request.POST)

    context = {
        "entry": comment_entry,
        "comments": comments,
    }


    if request.is_ajax():
        html = render_to_string("entries/comment.html", context, request=request)
        return JsonResponse({'form': html})


