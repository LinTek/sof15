# -*- coding: utf-8 -*-
from django.shortcuts import resolve_url
from django.views.generic import CreateView
from django.http import HttpResponseRedirect
from django.db import transaction
from django.forms.models import inlineformset_factory

from .models import Entry, EntryType, EntryMaterial, EntryCustomMaterial
from .forms import EntryForm, EntryFormHelper, EntryMaterialFormSetHelper


class EntryCreate(CreateView):
    form_class = EntryForm
    template_name = 'karthago/entries/create.html'

    def get_success_url(self):
        return resolve_url('karthago:create_kartege_entry_success')

    def get_context_data(self, **kwargs):
        context = super(EntryCreate, self).get_context_data(**kwargs)

        context['form_helper'] = EntryFormHelper()

        context['material_formset'] = inlineformset_factory(
            Entry,
            EntryMaterial,
            extra=20,
            can_delete=False,
            fields=('material', 'amount', 'role'))(self.request.POST or None)

        context['custom_material_formset'] = inlineformset_factory(
            Entry,
            EntryCustomMaterial,
            extra=10,
            can_delete=False,
            fields=('material', 'amount', 'unit', 'role'))(self.request.POST or None)

        context['material_formset_helper'] = EntryMaterialFormSetHelper()

        # Used by JS to view extra fields for free build
        context['free_build_pk'] = EntryType.objects.get(name__icontains='fribygge').pk

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        material_formset = context['material_formset']
        custom_material_formset = context['custom_material_formset']

        if material_formset.is_valid() and custom_material_formset.is_valid():
            with transaction.atomic():
                self.object = form.save()

                material_formset.instance = self.object
                material_formset.save()

                custom_material_formset.instance = self.object
                custom_material_formset.save()

            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))