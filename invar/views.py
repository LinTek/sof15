# -*- coding: utf-8 -*-
from django.views.generic import FormView, TemplateView
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from guardian.mixins import PermissionRequiredMixin

from invar.forms import BgMaxImportForm
from invar.models import Invoice, InvoiceRow


class BgMaxImportView(FormView):
    form_class = BgMaxImportForm
    success_url = reverse_lazy('admin:invar_transaction_import_bgmax')

    def form_valid(self, form):
        form.save()

        messages.success(self.request, _('Successfully imported transactions from BgMax file.'))
        return super(BgMaxImportView, self).form_valid(form)


class EconomicReportView(PermissionRequiredMixin, TemplateView):
    template_name = 'invar/economic_report.html'
    permission_required = 'invar.view_economic_report'
    accept_global_perms = True

    def get_context_data(self, **kwargs):
        context = super(EconomicReportView, self).get_context_data(**kwargs)
        context['summary'] = InvoiceRow.objects.filter(
            invoice__in=Invoice.objects.current()).report_summary()
        context['total_invoiced_amount'] = Invoice.objects.current().total_invoiced()
        context['total_payed_amount'] = Invoice.objects.current().total_payed()
        context['total_payed_invalidated_amount'] = Invoice.objects.invalidated().total_payed()
        context['fuzzy_matching_diff'] = Invoice.objects.current().payed().payed_diff()

        return context