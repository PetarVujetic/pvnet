from django.shortcuts import render, redirect
from .forms import RegistrationForm, UserProfileForm
from django.contrib.auth import authenticate, login
from .models import UserProfile
from entries.models import Entry
from django.views.generic import ListView
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from .models import Follower

def follow_user(request):
    """Follow button"""
    user_follow = get_object_or_404(User, pk = request.POST.get('pk'))
    is_following = False
    user = request.user

    if user_follow.userprofile.followers.all().filter(follower=user.userprofile).exists():
        is_following = False
        Follower.objects.filter(follower=user.userprofile, following=user_follow.userprofile).delete()
    else:
        is_following = True
        Follower.objects.create(follower=user.userprofile, following=user_follow.userprofile)

    followers_number = user_follow.userprofile.followers.all().count()
    following_number = user_follow.userprofile.following.all().count()
    user_follow_username = user_follow.userprofile.user.username

    context = {
        "user_follow":user_follow,
        "is_following":is_following,
        "username": user_follow_username,
        "followers_number": followers_number,
        "following_number": following_number
    }
    if request.is_ajax():
        html = render_to_string("users/follow.html", context, request=request)
        return JsonResponse({'form': html})




class ProfileView(ListView):
    """"View of users profile page with all his entries"""
    model = Entry
    template_name = 'users/profile.html'
    context_object_name = "profile_entries"
    paginate_by = 5

    def get_queryset(self):
        return Entry.objects.filter(entry_author_id=self.kwargs['pk']).order_by('-entry_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.filter(pk=self.kwargs['pk'])[0]
        is_following = user.userprofile.followers.all().filter(follower=self.request.user.userprofile).exists()
        followers_number = user.userprofile.followers.all().count()
        following_number = user.userprofile.following.all().count()
        context['followers_number'] = followers_number
        context['following_number'] = following_number
        context['entry_user'] = user
        context['is_following'] = is_following
        return context


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        userForm = UserProfileForm(request.POST)


        if form.is_valid() and userForm.is_valid():
            form.save()
            profile = userForm.save(commit=False)
            profile.user = form.save()
            profile.save()

            if 'image' in request.FILES:
                profile.image = request.FILES['image']
                profile.save()

            username = request.POST['username']
            password = request.POST['password1']
            user = authenticate(request, username = username, password = password)
            login(request, user)
            return redirect('blog-home')
    else:
        form = RegistrationForm()
        userForm = UserProfileForm()
    context = {'form':form, 'userForm':userForm}
    return render(request, 'users/register.html', context)

def login_view(request):
        context = {}
        if request.method =="POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username = username, password = password)
            if(user):
                login(request, user)
                return redirect('blog-home')
            else:
                context = {'error': "Username or password is incorrect."}

        return render(request, 'users/login.html', context)

class SearchView(ListView):
    model = User
    template_name = 'users/list_of_users.html'
    context_object_name = 'all_search_results'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_name = self.request.GET.get('search', '')
        context['all_search_results'] = User.objects.filter(username__icontains=user_name )
        return context

    def get_queryset(self):
       result = super(SearchView, self).get_queryset()
       query = self.request.GET.get('search')
       if query:
          postresult = User.objects.filter(username__contains=query)
          result = postresult
       else:
           result = None
       return result

def delete_entry(request):

    delete_pk = request.POST.get('pk')
    user_pk = request.user.pk

    Entry.objects.filter(pk = delete_pk).delete()
    
    profile_entries = Entry.objects.filter(entry_author_id=user_pk).order_by('-entry_date')
        
    context = {
        "profile_entries":profile_entries
    }
    
    if request.is_ajax():
        html = render_to_string("users/userEntries.html", context, request=request)
        return JsonResponse({'form': html})