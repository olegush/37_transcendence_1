from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings

from users import views


urlpatterns = [
    path('', views.DisplayWall.as_view(), name='index'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('id<int:pk>/', views.DisplayUser.as_view(), name='user'),
    path('id<int:pk>/add_to_friends/', views.UserAddToFriends.as_view()),
    path('id<int:pk>/remove_from_friends/', views.UserRemoveFromFriends.as_view()),
    path('profile/', views.UserUpdate.as_view(), name='profile'),
    path('wall/', views.DisplayWall.as_view(), name='wall'),
    path('subscriptions/', views.DisplaySubscriptions.as_view(), name='wall'),
    path('posts/', views.PostListView.as_view(), name='posts'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post'),
    path('post_add/', views.PostAdd.as_view(), name='post-add'),
    path('users/', views.UsersList.as_view(), name='users'),
    path('author/<int:pk>', views.PostListbyAuthorView.as_view(), name='posts-by-author'),


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
