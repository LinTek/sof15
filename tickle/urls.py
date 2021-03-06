# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from tickle.views.products import PurchaseView, ShoppingCartDeleteView, TurboDeliveryView, \
    TurboDeliveryAjaxView, add_to_shopping_cart, complete_purchase, ExchangeView, ConfirmExchangeView, cancel_transfer

urlpatterns = patterns(
    '',
    url(r'^purchase/$', PurchaseView.as_view(), name='purchase'),
    url(r'^purchase/complete/$', complete_purchase, name='complete_purchase'),
    url(r'^purchase/completed/$', TemplateView.as_view(template_name='tickle/purchase_completed.html'),
        name='purchase_completed_success'),

    url(r'^shoppingcart/add/(?P<pk>\d+)$', add_to_shopping_cart, name='shopping_cart_add'),
    url(r'^shoppingcart/remove/(?P<pk>\d+)$', ShoppingCartDeleteView.as_view(), name='shopping_cart_remove'),
    url(r'^purchase/transfer/(?P<pk>\d+)$', ExchangeView.as_view(), name='transfer_ticket'),
    url(r'^purchase/transfer/cancel/(?P<pk>\d+)$', cancel_transfer, name='cancel_transfer'),
    url(r'^purchase/transfer/confirm/(?P<pk>\d+)$', ConfirmExchangeView.as_view(), name='transfer_ticket_confirm'),
    url(r'^purchase/transfer/success$', TemplateView.as_view(template_name='tickle/transfer_success.html'),
        name='transfer_ticket_success'),
    url(r'^purchase/transfer/confirm/success$', TemplateView.as_view(template_name='tickle/transfer_confirm_success.html'),
        name='transfer_ticket_confirm_success'),

    url(r'^turbo-delivery/$', TurboDeliveryView.as_view(), name='turbo_delivery'),
    url(r'^turbo-delivery/ajax/$', TurboDeliveryAjaxView.as_view(), name='turbo_delivery_ajax'),
)
