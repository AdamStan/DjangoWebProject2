from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.
from .forms import UserAdminChangeForm, UserAdminCreationForm

User = get_user_model()

class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    list_display = ('username', 'password','admin','teacher','student','staff')
    list_filter = ('admin','teacher','student')

    fieldsets = (
        (None, {'fields': ('username','password')}),
        ('Personal Information', {'fields': ('name','surname','second_name') }),
        ('Permissions', {'fields': ('admin','student','teacher','staff') })
    )
    add_fieldsets = (
        (None, {
           'classes': ('wide'),
            'fields': ('username', 'password1', 'confirm_password', 'name', 'surname')}
        ),
    )
    search_fields = ('username', 'surname', 'name')
    filter_horizontal = ()

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
