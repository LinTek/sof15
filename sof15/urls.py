# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

from tickle.views.people import LoginView, ProfileView, ChangePasswordView, CreateUserView, IdentifyView
from fungus.views import ShiftChangeView
from invar.views import EconomicReportView

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'sof15.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', TemplateView.as_view(template_name='base.html'), name='root'),

    url(r'^people/login/$', LoginView.as_view(), name='login'),
    url(r'^people/change-password/$', ChangePasswordView.as_view(), name='change_password'),
    url(r'^people/create-account/$', CreateUserView.as_view(), name='create_user'),
    url(r'^people/create-account/success$', TemplateView.as_view(template_name='people/create_user_success.html'),
        name='create_user_success'),
    url(r'^people/logout/$', 'django.contrib.auth.views.logout', {'next_page': 'root'}, name='logout'),
    url(r'^people/(?P<pk>\d+)/$', ProfileView.as_view(), name='profile'),
    url(r'^people/me/$', LoginView.as_view(), name='profile_me'),

    url(r'^karthago/', include('karthago.urls', namespace='karthago', app_name='karthago')),
    url(r'^orchard/', include('orchard.urls', namespace='orchard', app_name='orchard')),
    url(r'^fungus/', include('fungus.urls', namespace='fungus', app_name='fungus')),
    url(r'^tickets/', include('tickle.urls', namespace='tickle', app_name='tickle')),
    url(r'^invar/economic-report/$', EconomicReportView.as_view(), name='economic_report'),

    url(r'^api/', include('api.urls', namespace='api')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^admin/fungus/shiftregistration/shifchange/$', ShiftChangeView.as_view(), name='change_selected_shifts'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/password_reset/$', auth_views.password_reset, name='admin_password_reset'),
    url(r'^admin/password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', auth_views.password_reset_confirm,
        name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),

    url(r'^i18n/', include('django.conf.urls.i18n')),
)
