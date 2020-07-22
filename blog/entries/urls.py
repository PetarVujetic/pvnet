from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from users import views

from .views import (CreateEntryView, EntryView, HomeView, createComment,
                    deleteComment, likePost)

urlpatterns = [
    path('', HomeView.as_view(), name='blog-home'),
    path('entry/<int:pk>/', EntryView.as_view(), name = 'entry-detail'),
    path('create_entry/', CreateEntryView.as_view(success_url='/'), name = 'create_entry'),
    path('comment/', createComment, name="createComment"),
    path('deleteComment/', deleteComment, name="deleteComment"),
    path('likePost/', likePost, name="likePost"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
