from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from core.mail import send_mail
import settings


def send_update_mails(ticket, ticket_update):
    assigned_sent = check_assigned_to(ticket)
    recipients = set([ticket.user.email])
    if not assigned_sent and ticket.assigned_to:
        recipients.remove(ticket.assigned_to.email)
        
    for update in ticket.updates.all():
        recipients.add(update.user.email)
    if ticket_update.public and ticket_update.comment:
        _send_to_clients(ticket, ticket_update)

    msg = _create_msg(ticket, ticket_update)
    send_mail(_("Ticket update"), msg, settings.NO_REPLY_EMAIL, recipients)

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
    msg = _("The ticket %s (%s) has been updated:") % (ticket.title, url)
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
        msg = _("You have been assigned to the ticket %s\nLink: %s") % (ticket.title, url)
    else:
        msg = _("You have been unassigned from the the ticket %s\nLink: %s u") % (ticket.title, url)

    send_mail(ticket.title, msg, settings.NO_REPLY_EMAIL, [user.email])
