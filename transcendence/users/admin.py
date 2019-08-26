from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db.models import Count
from django.utils.translation import gettext_lazy as _

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class FriendsQuantity(admin.SimpleListFilter):
    title = _('friends quantity')
    parameter_name = 'friends'
    def lookups(self, request, model_admin):
        return(
            ('0', _('no friends')),
            ('1-2', _('1..2')),
            ('>2', _('more than 2')),
        )
    def queryset(self, request, queryset):
        if self.value() == '0':
            return queryset.annotate(friends_count=Count('friends')).filter(friends_count__exact = 0)
        if self.value() == '1-2':
            return queryset.annotate(friends_count=Count('friends')).filter(friends_count__lte = 2)
        if self.value() == '>2':
            return queryset.annotate(friends_count=Count('friends')).filter(friends_count__gt = 2)


class ImageExistence(admin.SimpleListFilter):
    title = _('image existence')
    parameter_name = 'image'
    def lookups(self, request, model_admin):
        return(
            ('yes', _('yes')),
            ('no', _('no')),
        )
    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.exclude(image='')
        if self.value() == 'no':
            return queryset.filter(image='')


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'name', 'image', 'is_staff', 'is_active',)
    list_filter = (ImageExistence, FriendsQuantity,)
    fieldsets = (
        ('Info', {'fields': ('email', 'name', 'description', 'image', )}),
        ('Friends', {'fields': ('friends', )}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'description', 'image', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)
