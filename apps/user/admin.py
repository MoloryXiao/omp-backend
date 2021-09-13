from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from .models import OmpUser


class UserCreationForm(forms.ModelForm):

    class Meta:
        model = OmpUser
        fields = ('email', 'name')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = OmpUser
        fields = ('email', 'password', 'name', 'introduction', 'user_type', 'avatar', 'status')


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'name', 'introduction','user_type', 'avatar', 'status')
    list_filter = ('status',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('date_of_birth', 'name', 'introduction','user_type', 'avatar')}),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(OmpUser, UserAdmin)
admin.site.unregister(Group)
