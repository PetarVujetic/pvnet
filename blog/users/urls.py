from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
from . import views



urlpatterns = [
    path('profile/<int:pk>/', views.ProfileView.as_view(), name='profile'),
    path('users_search/', views.SearchView.as_view(), name='user_search'),
    path('register/', views.register, name = 'register'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('follow/', views.follow_user, name="follow_user"),
    path('delete/', views.delete_entry, name="delete_entry")

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
