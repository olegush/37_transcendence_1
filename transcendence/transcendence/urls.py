from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings

from users import views


urlpatterns = [
    path('', views.MyPostsList.as_view(), name='index'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('id<int:pk>/', views.UserDisplay.as_view(), name='user'),
    path('id<int:pk>/add_to_friends/', views.UserAddToFriends.as_view()),
    path('id<int:pk>/remove_from_friends/', views.UserRemoveFromFriends.as_view()),
    path('profile/', views.UserUpdate.as_view(), name='profile'),
    path('my_posts/', views.MyPostsList.as_view(), name='my_posts'),
    path('subscriptions/', views.SubscriptionsList.as_view(), name='subscriptions'),
    path('bookmarks/', views.BookmarksList.as_view(), name='bookmarks'),
    path('all_posts/', views.AllPostsList.as_view(), name='posts'),
    path('post/<int:pk>/', views.PostDetail.as_view(), name='post'),
    path('post_add/', views.PostAdd.as_view(), name='post-add'),
    path('post/<int:pk>/bookmark/', views.PostToBookmark.as_view(), name='post-to-bookmark'),
    path('users/', views.UsersList.as_view(), name='users'),
    path('author/<int:pk>', views.PostListbyAuthor.as_view(), name='posts-by-author'),


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
