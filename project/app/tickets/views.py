# -*- coding: utf-8 -*-
from django.conf import settings
from app.client.models import ClientUser
from app.tickets.models import Ticket, TicketUpdate, TicketType
from core import Core
from core.decorators import require_permission, login_required
from django.shortcuts import render, get_object_or_404
from app.tickets.forms import TicketForm, EditTicketForm, AddTicketTypeForm, AddClientForm
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from django.utils import simplejson
from django.http import HttpResponse
from core.mail import send_mail
import copy

@require_permission("LIST", Ticket)
def overview(request):
    tickets = Core.current_user().get_permitted_objects("VIEW", Ticket).\
    filter(trashed=False).order_by('title')

    return render(request, 'tickets/list.html',
            {"title": "Tickets", 'tickets': tickets})


@require_permission("LIST", Ticket)
def assigned_to_user(request):
    tickets = Core.current_user().get_permitted_objects("VIEW", Ticket).\
    filter(trashed=False, assigned_to=request.user).order_by("status", "-priority", "-date_edited")

    return render(request, 'tickets/list.html', {"title": "Tickets",
                                                 "assigned_to": True,
                                                 'tickets': tickets})

@require_permission("LIST", Ticket)
def overview_trashed(request):
    tickets = Core.current_user().get_permitted_objects("VIEW", Ticket).filter(trashed=True).order_by("status",
                                                                                                      "-priority",
                                                                                                      "-date_edited")

    return render(request, 'tickets/list.html',
            {"title": "Tickets", 'tickets': tickets})


@require_permission("VIEW", Ticket, "id")
def trash(request, id):
    ticket = Ticket.objects.get(id=id)

    if request.method == "POST":
        if not ticket.can_be_deleted()[0]:
            request.message_error("You can't delete this ticket because: ")
            for reason in ticket.can_be_deleted()[1]:
                request.message_error(reason)
        else:
            request.message_success("Successfully deleted this ticket")
            ticket.trash()
        return redirect(overview)
    else:
        return render(request, 'tickets/trash.html', {'title': _("Confirm delete"),
                                                      'ticket': ticket,
                                                      'can_be_deleted': ticket.can_be_deleted()[0],
                                                      'reasons': ticket.can_be_deleted()[1],
                                                      })


@require_permission("VIEW", Ticket)
def add(request):
    return form(request)


def create_update_for_ticket(old_ticket, ticket_form):
    ticket, ticket_update = ticket_form.save(commit=False)
    ticket_update.user = Core.current_user()
    ticket_update.company = ticket.company
    ticket_update.save()
    differences = Ticket.find_differences(ticket, old_ticket)
    ticket_update.create_update_lines(differences)
    ticket.save(update=ticket_update)
    return ticket


@require_permission("VIEW", Ticket, "id")
def edit(request, id):
    ticket = Core.current_user().get_permitted_objects("VIEW", Ticket).get(id=id)
    updates = TicketUpdate.objects.filter(ticket=ticket).order_by("-id")

    #ticket.visited_by_since_last_edit.add((Core.current_user()))

    if request.method == "POST":
        old_ticket = copy.copy(ticket)
        ticket_form = EditTicketForm(request.POST, request.FILES, instance=ticket)

        if ticket_form.is_valid():
            ticket = create_update_for_ticket(old_ticket, ticket_form)

            ticket.invalidate_cache()

            request.message_success(_("Ticket updated"))

            return redirect(edit, ticket.id)

    else:
        ticket_form = EditTicketForm(instance=ticket)

    return render(request, "tickets/edit.html", {'title': _('Update Ticket'),
                                                 'ticket': ticket,
                                                 'updates': updates,
                                                 'form': ticket_form,
                                                 })


@login_required()
def form(request, id=False):
    if id:
        instance = Core.current_user().get_permitted_objects("VIEW", Ticket).get(id=id)
        msg = _("Ticket changed")
    else:
        instance = Ticket()
        msg = _("Ticket added")

    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.set_user(Core.current_user())
            ticket.save()
            request.message_success(msg)

            return redirect(edit, ticket.id)
    else:
        form = TicketForm(instance=instance)

    return render(request, "tickets/form.html", {'title': _('Ticket'),
                                                 'ticket': instance,
                                                 'form': form,
                                                 })


@require_permission("CREATE", Ticket)
def add_ticket_type_ajax(request, id=None):
    if id:
        instance = get_object_or_404(TicketType, id=id)
    else:
        instance = TicketType()
    form = AddTicketTypeForm(request.POST, instance=instance)
    if form.is_valid():
        ticket_type = form.save(commit=False)
        ticket_type.company = Core.current_user().get_company()
        ticket_type.save()

        return HttpResponse(simplejson.dumps({'name': ticket_type.name,
                                              'id': ticket_type.id,
                                              'valid': True}), mimetype='application/json')
    else:
        errors = dict([(field, errors[0]) for field, errors in form.errors.items()])
        return HttpResponse(simplejson.dumps({'errors': errors,
                                              'valid': False}), mimetype='application/json')


@require_permission("CREATE", Ticket)
def ajax_change_update_visibility(request):
    if request.is_ajax() and request.method == 'POST':
        id = request.POST['id']
        update = get_object_or_404(TicketUpdate, id=id)
        if request.POST.get('visible', False) == '1':
            update.public = True
        else:
            update.public = False
        update.save()

        return HttpResponse(simplejson.dumps({'visible': update.public}))

    return HttpResponse(status=400)


@require_permission("VIEW", Ticket, "id")
def client_management(request, id):
    ticket = Ticket.objects.get(id=id)

    if request.method == "POST":
        form = AddClientForm(request.POST)

        if form.is_valid():
            email_address = request.POST['email']
            client, created = ClientUser.objects.get_or_create(email=email_address)

            client.tickets.add(ticket)
            client.save() # not needed?

            if created:
                password = client.generate_password()
                client.set_password(password)
                client.save()
                password_text = "Bruk din epostadresse og passord: %s" % password

            else:
                password_text = "Bruk din epostadresse og passord fra tidligere. Du kan også be om å få tilsendt nytt."

            message = """
            Hei. Du har fått tilgang til å følge en sak hos oss. Logg inn på %s for å se detaljer.

            %s

            """ % (settings.CLIENT_LOGIN_SITE, password_text)
            send_mail(_("New ticket"), message, settings.NO_REPLY_EMAIL, [email_address])

    else:
        form = AddClientForm()

    return render(request, "tickets/client_management.html", {'ticket': ticket, 'form': form})