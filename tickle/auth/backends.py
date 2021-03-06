# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.backends import ModelBackend
from django.db.transaction import atomic
from django.db import IntegrityError

from django_auth_ldap.backend import LDAPBackend

from tickle.models import TickleUser, Person
from tickle.auth.settings import LiUStudentLDAPSettings, LiUEmployeeLDAPSettings

import logging
logger = logging.getLogger(__name__)


class _LiUBaseLDAPBackend(LDAPBackend):
    """
    DON'T USE THIS AS YOUR AUTH BACKEND! Use the LiUStudentBackend and/or LiUEmployeeBackend instead.
    """

    def _get_settings(self):
        """
        Overridden since the _settings are always set in our subclasses.
        """

        return self._settings

    def populate_person_data(self, person, ldap_user):
        """
        Feel free to override this in your subclass. You don't have to save the person object, we'll do it later.
        """

        person.first_name = ldap_user.attrs['givenName'][0]
        person.last_name = ldap_user.attrs['sn'][0]

        return person

    def get_or_create_person(self, username, ldap_user):
        liu_id = ldap_user.attrs['cn'][0]
        email = ldap_user.attrs['mail'][0]

        try:
            person = Person.objects.get(email=email)
            person.liu_id = liu_id
            created = False
        except Person.DoesNotExist:
            try:
                person = Person.objects.get(liu_id=liu_id)
                created = False
            except Person.DoesNotExist:
                person = Person(liu_id=liu_id, email=email)
                created = True

        return person, created

    def get_or_create_user(self, username, ldap_user):
        with atomic():
            person, person_created = self.get_or_create_person(username, ldap_user)

            # Runs any subclass specific logic for populating the Person object with extra data.
            person = self.populate_person_data(person, ldap_user)

            person.save()

            return TickleUser.objects.get_or_create(person=person)

    def get_group_permissions(self, user, obj=None):
        # A hack resolving issues with using TickleUser.person (a ForeignKey) as USERNAME_FIELD. We don't use LDAP group
        # permissions anyway.
        return set()


class LiUStudentLDAPBackend(_LiUBaseLDAPBackend):
    """
    An authentication backend for LiU students.
    """

    settings_prefix = 'LIU_STUDENT_LDAP_'
    _settings = LiUStudentLDAPSettings(settings_prefix)

    def get_or_create_user(self, username, ldap_user):
        person, person_created = self.get_or_create_person(username, ldap_user)

        # Runs any subclass specific logic for populating the Person object with extra data.
        person = self.populate_person_data(person, ldap_user)
        person = person.fill_kobra_data(overwrite_name=False)
        try:
            person.save()
        except IntegrityError:
            person = Person.objects.get(birth_date=person.birth_date, pid_code=person.pid_code,
                                        pid_coordination=person.pid_coordination)
            person = person.fill_kobra_data(save=True, overwrite_name=False)

        return TickleUser.objects.get_or_create(person=person)


class LiUEmployeeLDAPBackend(_LiUBaseLDAPBackend):
    """
    An authentication backend for LiU employees.
    """

    settings_prefix = 'LIU_EMPLOYEE_LDAP_'
    _settings = LiUEmployeeLDAPSettings(settings_prefix)


class TickleBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        """
        Authenticates users against their email address.
        """
        try:
            user = TickleUser.objects.get(person__email__exact=username)
            if user.check_password(password):
                return user

        except TickleUser.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (#20760).
            TickleUser().set_password(password)
