#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

import csv
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django_tables2 import RequestConfig
from rapidsms.models import Contact, Connection, Backend
from rapidsms.contrib.registration.tables import ContactTable
from rapidsms.contrib.registration.forms import (
    BulkRegistrationForm,
    ContactForm, ConnectionFormSet)


def registration(request):
    contacts_table = ContactTable(
        Contact.objects.all(),
        template="django_tables2/bootstrap-tables.html")
    RequestConfig(request, paginate={"per_page": 25}).configure(contacts_table)
    return render(request, "registration/dashboard.html", {
        "contacts_table": contacts_table,
    })


def contact(request, pk=None):
    if pk:
        contact = get_object_or_404(Contact, pk=pk)
    else:
        contact = None
    contact_form = ContactForm(instance=contact)
    connection_formset = ConnectionFormSet(instance=contact)
    if request.method == 'POST':
        data = {}
        for key in request.POST:
            val = request.POST[key]
            if isinstance(val, basestring):
                data[key] = val
            else:
                try:
                    data[key] = val[0]
                except (IndexError, TypeError):
                    data[key] = val
        # print repr(data)
        del data
        if pk:
            if request.POST["submit"] == "Delete Contact":
                contact.delete()
                return HttpResponseRedirect(reverse(registration))
            contact_form = ContactForm(request.POST, instance=contact)
        else:
            contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            contact = contact_form.save(commit=False)
            connection_formset = ConnectionFormSet(request.POST,
                                                   instance=contact)
            if connection_formset.is_valid():
                contact.save()
                connection_formset.save()
                return HttpResponseRedirect(reverse(registration))
    return render(request, 'registration/contact_form.html', {
        "contact": contact,
        "contact_form": contact_form,
        "connection_formset": connection_formset,
        })


@transaction.commit_on_success
def contact_bulk_add(request):
    bulk_form = BulkRegistrationForm(request.POST)

    if request.method == "POST" and "bulk" in request.FILES:
        reader = csv.reader(
            request.FILES["bulk"],
            quoting=csv.QUOTE_NONE,
            skipinitialspace=True
        )
        count = 0
        for i, row in enumerate(reader, start=1):
            try:
                name, backend_name, identity = row
            except:
                return render(request, 'registration/bulk_form.html', {
                    "bulk_form": bulk_form,
                    "csv_errors": "Could not unpack line " + str(i),
                })
            contact = Contact.objects.create(name=name)
            try:
                backend = Backend.objects.get(name=backend_name)
            except:
                return render(request, 'registration/bulk_form.html', {
                    "bulk_form": bulk_form,
                    "csv_errors": "Could not find Backend.  Line: " + str(i),
                })
            connection = Connection.objects.create(
                backend=backend,
                identity=identity,
                contact=contact)
            count += 1
        if not count:
            return render(request, 'registration/bulk_form.html', {
                "bulk_form": bulk_form,
                "csv_errors": "No contacts found in file",
            })
        return HttpResponseRedirect(reverse(registration))
    return render(request, 'registration/bulk_form.html', {
        "bulk_form": bulk_form,
    })
