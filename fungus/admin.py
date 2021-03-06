# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.utils.translation import ugettext
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect
from django.db.models import Q

from tickle.models import Person
from fungus.models import ShiftType, Shift, ShiftRegistration, Functionary, Worker, FunctionaryDiscount, \
    FunctionaryShiftTypeDiscount
from tickle.admin import PersonAdmin, TickleUserInline, PurchaseInline


@admin.register(ShiftType)
class ShiftTypeAdmin(admin.ModelAdmin):
    pass


class ShiftRegistrationInline(admin.TabularInline):
    model = ShiftRegistration
    extra = 0

    raw_id_fields = ('person',)


class ResponsibleListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('responsible person')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'responsible'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        people = set([i.responsible for i in model_admin.model.objects.filter(responsible__isnull=False)])
        return [(i.pk, i.full_name) for i in people]

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value():
            return queryset.filter(responsible__pk__exact=self.value())
        else:
            return queryset


class ShiftTypeListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('shift type')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'shift_type'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        shift_types = set([i.shift_type for i in model_admin.model.objects.all()])
        return [(i.pk, i.__str__) for i in shift_types]

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value():
            return queryset.filter(shift_type__pk__exact=self.value())
        else:
            return queryset


class ShiftStatusListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('status')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('critical', _('Critical')),
            ('alarming', _('Alarming')),
            ('ok', _('OK')),
            ('overstaffed', _('Overstaffed'))
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value() == 'critical':
            return queryset.critical()
        elif self.value() == 'alarming':
            return queryset.alarming()
        elif self.value() == 'ok':
            return queryset.ok()
        elif self.value() == 'overstaffed':
            return queryset.overstaffed()
        else:
            return queryset


@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    inlines = (ShiftRegistrationInline,)

    date_hierarchy = 'start'
    list_display = ('shift_type', 'start', 'end', 'rendered_registrations', 'people_critical', 'people_alarming', 'people_max', 'responsible', 'public')
    list_display_links = ('shift_type', 'start', 'end')
    list_editable = ('people_max', 'people_alarming', 'people_critical', 'public')
    list_filter = (ShiftTypeListFilter, ShiftStatusListFilter, 'public', ResponsibleListFilter)

    def rendered_registrations(self, obj):
        registrations = obj.registrations.count()
        status = obj.status

        if status == 'critical':
            return '{0}&nbsp;&nbsp;&nbsp;&nbsp;<strong style="color: #ff0000;">{1}</strong>'.format(registrations, ugettext('Critical'))
        elif status == 'alarming':
            return '{0}&nbsp;&nbsp;&nbsp;&nbsp;<strong style="color: #ffc000;">{1}</strong>'.format(registrations, ugettext('Alarming'))
        elif status == 'ok':
            return '{0}&nbsp;&nbsp;&nbsp;&nbsp;<strong style="color: #48ac3b;">{1}</strong>'.format(registrations, ugettext('OK'))
        elif status == 'overstaffed':
            return '{0}&nbsp;&nbsp;&nbsp;&nbsp;<strong style="color: #48ac3b;">{1}</strong>'.format(registrations, ugettext('Overstaffed'))

    rendered_registrations.short_description = _('status')
    rendered_registrations.allow_tags = True


class ShiftRegistrationPersonListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('person')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'person'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        people = set([i.person for i in model_admin.model.objects.all()])
        return [(i.pk, i.full_name) for i in people]

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value():
            return queryset.filter(person__pk__exact=self.value())
        else:
            return queryset


@admin.register(ShiftRegistration)
class ShiftRegistrationAdmin(admin.ModelAdmin):
    list_display = ('person', 'shift', 'checked_in', 'checked_out')
    list_filter = (ShiftRegistrationPersonListFilter,)
    list_editable = ('checked_in', 'checked_out')
    search_fields = ('person__liu_card_rfid', 'person__liu_id', 'person__first_name', 'person__last_name', 'person__pid_code')

    actions = ['change_pass_action']

    def change_pass_action(self, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        return HttpResponseRedirect("shifchange/?ids=%s" % ",".join(selected))

    change_pass_action.short_description = "Byt markerade arbetspass"


class FunctionaryInline(admin.StackedInline):
    model = Functionary
    extra = 0
    max_num = 1


class ShiftListFilter(admin.SimpleListFilter):
    title = _('shift')

    parameter_name = 'shift'

    def lookups(self, request, model_admin):
        return [(i.pk, i) for i in Shift.objects.all()]

    def queryset(self, request, queryset):
        if self.value():
            shift = Shift.objects.get(pk=self.value())
            return queryset.filter(shift_registrations__shift=shift)
        else:
            return queryset


@admin.register(Worker)
class WorkerAdmin(PersonAdmin):
    change_list_template = 'admin/tickle/person/change_list.html'
    inlines = (FunctionaryInline, ShiftRegistrationInline, TickleUserInline, PurchaseInline,)
    list_display = ('first_name', 'last_name', 'pid', 'email', 'phone', 'liu_id', 'registration_count',
                    'functionary_registered', 'functionary_signed_contract', 'functionary_attended_info_meeting',
                    'functionary_pledge_payed', 'functionary_pledge_returned', 'special_nutrition_render', 'notes')

    list_filter = ('special_nutrition', ShiftListFilter)

    def get_queryset(self, request):
        """
        Returns the original queryset but filters out only registered workers and people with shift registrations
        """
        return super(WorkerAdmin, self).get_queryset(request).workers()

    def functionary_registered(self, obj):
        return obj.functionary.registered or None

    functionary_registered.short_description = _('functionary registered')
    functionary_registered.admin_order_field = 'functionary__registered'

    def functionary_signed_contract(self, obj):
        return obj.functionary.signed_contract or None

    functionary_signed_contract.short_description = _('signed contract')
    functionary_signed_contract.admin_order_field = 'functionary__signed_contract'

    def functionary_attended_info_meeting(self, obj):
        return obj.functionary.attended_info_meeting or None

    functionary_attended_info_meeting.short_description = _('attended info meeting')
    functionary_attended_info_meeting.admin_order_field = 'functionary__attended_info_meeting'

    def functionary_pledge_payed(self, obj):
        return obj.functionary.pledge_payed or None

    functionary_pledge_payed.short_description = _('pledge payed')
    functionary_pledge_payed.admin_order_field = 'functionary__pledge_payed'

    def functionary_pledge_returned(self, obj):
        return obj.functionary.pledge_returned or None

    functionary_pledge_returned.short_description = _('pledge returned')
    functionary_pledge_returned.admin_order_field = 'functionary__pledge_returned'

    def registration_count(self, obj):
        return obj.shift_registrations.count()

    registration_count.short_description = _('shifts')


@admin.register(FunctionaryDiscount)
class FunctionaryDiscountAdmin(admin.ModelAdmin):
    pass


@admin.register(FunctionaryShiftTypeDiscount)
class FunctionaryShiftTypeDiscountAdmin(admin.ModelAdmin):
    filter_horizontal = ('shift_types',)
