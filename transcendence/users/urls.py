from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.urls import path, include

from . import views

urlpatterns = [
    #path('accounts/', include('django.contrib.auth.urls')),
    #path('', views.show_user, name='user'),
    #views.wall

    #path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    #path('', views.show_user, name='user'),
    #path('accounts/', include('users.urls')),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

print(urlpatterns)
