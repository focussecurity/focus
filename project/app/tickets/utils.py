# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from core import Core
from core.mail import send_mail
from django.conf import settings
import hashlib

def send_update_mails(ticket, ticket_update):
    """
    Sends email to all users who commented or created ticket
    """
    assigned_sent = check_assigned_to(ticket)

    recipients = set([])

    if not ticket.mailbox_hash:

        ticket.mailbox_hash = hashlib.sha224("ticket-%s"%ticket.id).hexdigest()
        ticket.save()

    if ticket.assigned_to:
        if ticket.assigned_to.email:
            recipients.add(ticket.assigned_to.email)

    if not assigned_sent and ticket.assigned_to:
        if ticket.assigned_to.email in recipients:
            recipients.remove(ticket.assigned_to.email)

    for recipient in ticket.get_recipients():
        if recipient.email:
            recipients.add(recipient.email)

    if Core.current_user().email:
        if Core.current_user().email in recipients:
            recipients.remove(Core.current_user().email)

    if ticket_update.public and ticket_update.comment:
        _send_to_clients(ticket, ticket_update)

    msg = _create_msg(ticket, ticket_update)
    send_mail(_("Ticket update"), msg, "support+"+ticket.mailbox_hash+"@focustime.no", recipients)

def _send_to_clients(ticket, ticket_update):
    recipients = [client.email for client in ticket.clients.all()]
    msg = _create_client_msg(ticket, ticket_update)
    send_mail(_("Ticket update"), msg, settings.NO_REPLY_EMAIL, recipients)

def _create_msg(ticket, ticket_update):
    msg = _create_client_msg(ticket, ticket_update)
    update_lines = ticket_update.update_lines.all()
    if update_lines:
        msg += "\n\n" + _("Changes: \n")
        for line in update_lines:
            msg += "\t" + line.change + "\n"

    return msg

def _create_client_msg(ticket, ticket_update):
    url = settings.SITE_URL + reverse("ticket_view", kwargs={'id': ticket.id})
    msg = "------------------------------------------------------------------------------------------------\n"
    msg += ("%s %s (%s) %s:") % (_("The ticket "), ticket.title, url, _("has been updated"))
    if ticket_update.comment:
        msg += "\n\n" + _("Comment:") + "\n%s" % ticket_update.comment

    return msg


def check_assigned_to(ticket):
    cls = ticket.__class__
    try:
        old = cls.objects.get(id=ticket.id).assigned_to
    except cls.DoesNotExist:
        old = False

    if not old == ticket.assigned_to:
        if ticket.assigned_to:
            send_assigned_mail(ticket.assigned_to, ticket)
        if old:
            send_assigned_mail(old, ticket, assigned=False)
        return True

    return False


def send_assigned_mail(user, ticket, assigned=True):
    if not user.email:
        return
    url = settings.SITE_URL + reverse("ticket_view", kwargs={'id': ticket.id})

    if assigned:
        msg = (" %s %s \n %s: %s \n\n") % (_("You have been assigned to the ticket"),ticket.title, _("Link"), url)
    else:
        msg = (" %s %s \n %s: %s \n\n") % (_("You have been unassigned to the ticket"),ticket.title, _("Link"), url)

    msg += _("Description") + "\n" + ticket.description

    send_mail(ticket.title, msg, settings.NO_REPLY_EMAIL, [user.email])