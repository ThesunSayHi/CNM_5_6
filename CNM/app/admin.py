from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Posts, Profile, Wallet, PostImage

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['id', 'username', 'is_staff', 'is_active', 'is_posters']
    list_filter = ['is_staff', 'is_active', 'is_posters']
    fieldsets = (
        ('Account Information', {'fields': ('username', 'password')}),
        ('Personal information', {'fields': ('name',)}),
        ('Rights', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_posters', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    search_fields = ('username',)
    ordering = ('id',)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser', 'is_posters')
        }),
    )

admin.site.register(Profile)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Posts)
admin.site.register(Wallet)
admin.site.register(PostImage)
