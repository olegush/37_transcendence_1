from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings

from users import views as user_views
from posts import views as posts_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),

    path('', posts_views.MyPostsList.as_view(), name='index'),
    
    path('id<int:pk>/', user_views.UserDisplay.as_view(), name='user'),
    path('id<int:pk>/add_to_friends/', user_views.UserAddToFriends.as_view()),
    path('id<int:pk>/remove_from_friends/', user_views.UserRemoveFromFriends.as_view()),
    path('profile/', user_views.UserUpdate.as_view(), name='profile'),
    path('users/', user_views.UsersList.as_view(), name='users'),

    path('my_posts/', posts_views.MyPostsList.as_view(), name='my_posts'),
    path('subscriptions/', posts_views.SubscriptionsList.as_view(), name='subscriptions'),
    path('bookmarks/', posts_views.BookmarksList.as_view(), name='bookmarks'),
    path('all_posts/', posts_views.AllPostsList.as_view(), name='posts'),
    path('post/<int:pk>/', posts_views.PostDetail.as_view(), name='post'),
    path('post_add/', posts_views.PostAdd.as_view(), name='post-add'),
    path('post/<int:pk>/bookmark/', posts_views.PostToBookmark.as_view(), name='post-to-bookmark'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
