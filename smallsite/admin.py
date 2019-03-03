from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import CustomUser, UserProfileInfo, Subject
from .forms import CustomUserAdminChangeForm, CustomUserAdminCreationForm


class CustomUserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = CustomUserAdminChangeForm
    add_form = CustomUserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'admin')
    list_filter = ('admin', 'active', 'staff')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        # ('Personal info', {'fields': ()}),
        ('Permissions', {'fields': ('admin', 'active', 'staff')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserProfileInfo)
admin.site.register(Subject)
admin.site.unregister(Group)
