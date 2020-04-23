from django.urls import path, include
from .views import HomeView, EntryView, CreateEntryView
from django.conf.urls.static import static
from django.conf import settings
from users import views

urlpatterns = [
    path('', HomeView.as_view(), name='blog-home'),
    path('enrty/<int:pk>/', EntryView.as_view(), name = 'entry-detail'),
    path('create_entry/', CreateEntryView.as_view(success_url='/'), name = 'create_entry'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
