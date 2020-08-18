from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.views.generic import ListView

from entries.models import Entry

from .forms import RegistrationForm, UserProfileForm
from .models import Follower, Notification, NotificationHistory, UserProfile


def follow_user(request):
    """Follow button"""
    user_follow = get_object_or_404(User, pk = request.POST.get('pk'))
    is_following = False
    user = request.user

    Notification.objects.create(notified_user=user_follow, notification_type="follow", notification_maker=user)

    if user_follow.userprofile.followers.all().filter(follower=user.userprofile).exists():
        is_following = False
        Follower.objects.filter(follower=user.userprofile, following=user_follow.userprofile).delete()
        Notification.objects.filter(notified_user=user_follow, notification_type="follow", notification_maker=user).delete()
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
    context = {}
    if request.method == "POST":
        context['username'] = request.POST['username']
        context['email'] = request.POST['email']

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
            Notification.objects.create(notified_user=user, notification_type="welcome")
            return redirect('blog-home')
    else:
        form = RegistrationForm()
        userForm = UserProfileForm()
    context['form'] = form
    context['userForm'] = userForm
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

def followers(request, pk):
    user = get_object_or_404(User, pk = pk)
    context = {}
    lista = []
    followers = Follower.objects.filter(following=user.userprofile)
    
    for i in followers:
        lista += [i.follower.user]
    context['followers'] = lista
    context['user'] = user
    return render(request, 'users/followers.html', context)
    
def following(request, pk):
    user = get_object_or_404(User, pk = pk)
    context = {}
    lista = []
    following = Follower.objects.filter(follower=user.userprofile)

    for i in following:
        lista += [i.following.user]
        
    context['following'] = lista
    context['user'] = user
    return render(request, 'users/following.html', context)

def profile_edit(request):

    if request.method == "POST":
        context = {}
        user = request.user
        email = request.POST['email']
        username = request.POST['username']
        followers_number = user.userprofile.followers.all().count()
        following_number = user.userprofile.following.all().count() 


        context['entry_user'] = user
        context['followers_number'] = followers_number
        context['following_number'] = following_number

        if not username == user.username:
            if User.objects.all().filter(username=username).exists():
                context['usernameerror'] = "A user with that username already exists"
                return render(request, 'users/profileEdit.html', context)
            else:
                user.username = username
                user.save() 

        if 'image' in request.FILES:
            image = request.FILES['image']
            user.userprofile.image = image
            user.userprofile.save()

        user.email = email
        user.save()

       

        

        return redirect('profile', user.pk)

    context = {}
    user = request.user

    if not user:
        return redirect('welcome')

    followers_number = user.userprofile.followers.all().count()
    following_number = user.userprofile.following.all().count() 


    context['entry_user'] = user
    context['followers_number'] = followers_number
    context['following_number'] = following_number
    return render(request, 'users/profileEdit.html', context)

def notifications(request):
    context = {}
    notifications = []
    notifications_history = []

    if(request.user.is_authenticated):
        user = request.user 

        notifications_history = NotificationHistory.objects.all().filter(notified_user = user)

        for i in Notification.objects.all().filter(notified_user = user):
            notifications += [i]
            if(i.notification_type!="welcome"):
                NotificationHistory.objects.create(notified_user=i.notified_user, notification_type=i.notification_type, notification_maker=i.notification_maker, commented_post = i.commented_post)
            i.delete()

        
        context = {'notifications' : notifications, 'notifications_history': notifications_history}
    return render(request, 'users/notifications.html', context)

def profile_delete(request):
    user = request.user 
    logout(request)
    user.delete()
    return redirect('welcome')
