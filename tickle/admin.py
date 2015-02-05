# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms

from django.contrib.auth.models import Permission
from tickle.models import Person, Event, Product, Holding, TicketType, Delivery, Purchase, SpecialNutrition, TickleUser


class PurchaseInline(admin.StackedInline):
    model = Purchase
    # filter_horizontal = ('holdings',)




@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Holding)
class HoldingAdmin(admin.ModelAdmin):
    pass


@admin.register(TicketType)
class TicketTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    pass


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    pass


@admin.register(SpecialNutrition)
class SpecialNutritionAdmin(admin.ModelAdmin):
    pass


class TickleUserAdminForm(forms.ModelForm):
    class Meta:
        model = TickleUser
        fields = ('person', 'is_active', 'is_admin')


@admin.register(TickleUser)
class TickleUserAdmin(UserAdmin):
    form = TickleUserAdminForm
    add_form = TickleUserAdminForm
    fieldsets = (
        (None, {'fields': ('person', )}),
        ('Permissions', {'fields': ('groups', 'user_permissions')}),
        ('Stuff', {'fields': ('is_active', 'is_admin', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {'fields': ('person', )}),
        ('Permissions', {'fields': ('groups', 'user_permissions')}),
        ('Stuff', {'fields': ('is_active', 'is_admin', 'is_superuser')}),
    )

    list_display = ('person', 'is_active', 'is_admin')
    list_filter = ('is_admin', 'is_superuser', 'is_active', 'groups')
    raw_id_fields = ('person',)

    def save_model(self, request, obj, form, change):
        obj.person.save()
        super(TickleUserAdmin, self).save_model(request, obj, form, change)

class AlwaysChangedModelForm(forms.ModelForm):
    def has_changed(self):
        return True


class TickleUserInline(admin.StackedInline):
    model = TickleUser
    form = AlwaysChangedModelForm  # This way we can just press Add, not change anything and still get an account created
    extra = 0
    max_num = 1

    exclude = ('username', 'password',)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    inlines = (TickleUserInline, PurchaseInline,)

    list_display = ('first_name', 'last_name', 'pid', 'email', 'phone', 'liu_id')
    list_display_links = ('first_name', 'last_name', 'pid')
    list_filter = ('special_nutrition',)

    search_fields = ('first_name', 'last_name', 'email', 'liu_id__liu_id')

@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    pass