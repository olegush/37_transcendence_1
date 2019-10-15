from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings

from . import views
from users import views as users_views


urlpatterns = [
    path('', views.index),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('id<int:pk>/', users_views.DisplayUser.as_view(), name='user'),
    path('id<int:pk>/add_to_friends/', users_views.UserAddToFriends.as_view()),
    path('id<int:pk>/remove_from_friends/', users_views.UserRemoveFromFriends.as_view()),
    path('profile/', users_views.UserUpdate.as_view(), name='profile'),
    path('wall/', users_views.DisplayWall.as_view(), name='wall'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
