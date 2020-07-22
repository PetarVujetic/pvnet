from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.views.generic import CreateView, DetailView, ListView

from .models import Comment, Entry


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
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)     
        for entry in context['blog_entries']:
            context['entry.pk'] = entry.entry_likes.all().count()
        return context

class EntryView(LoginRequiredMixin, DetailView):
    model = Entry
    template_name = 'entries/entry_detail.html'
    context_object_name = "entry"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = Comment.objects.filter(comment_entry = context['entry'])
        context['comments'] = comments
        
        if(context['entry'].entry_likes.filter(pk=self.request.user.pk).exists()):
            context['is_liked'] = True
        else:
            context['is_liked'] = False

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
    error = False
    if(comment_text!=""):
        Comment.objects.create(comment_author=comment_author, comment_entry=comment_entry, comment_text = comment_text)
    else:
        error = "Comment text can't be empty!"
    
    comments = Comment.objects.filter(comment_entry=comment_entry)
    print(request.POST)

    context = {
        "error": error,
        "entry": comment_entry,
        "comments": comments,
    }
    if request.is_ajax():
        html = render_to_string("entries/comment.html", context, request=request)
        return JsonResponse({'form': html})

def deleteComment(request):
    comment = get_object_or_404(Comment, pk = request.POST.get('pk'))
    comment_entry = comment.comment_entry
    comment.delete()
    comments = Comment.objects.filter(comment_entry=comment_entry)

    context = {
        "entry": comment_entry,
        "comments": comments,
    }

    if request.is_ajax():
        html = render_to_string("entries/comment.html", context, request=request)
        return JsonResponse({'form': html})

def likePost(request):

    entry = get_object_or_404(Entry, pk = request.POST.get('pk'))

    if(entry.entry_likes.filter(pk=request.user.pk).exists()):
        entry.entry_likes.remove(request.user)
        is_liked = False
    else:
        entry.entry_likes.add(request.user)
        is_liked = True
    likes_number = entry.entry_likes.all().count()

    context = {
        "is_liked": is_liked,
        "entry":  entry,
        "likes_number":likes_number,
    }

    if request.is_ajax():
        html = render_to_string("entries/likesystem.html", context, request=request)
        return JsonResponse({'form': html})
