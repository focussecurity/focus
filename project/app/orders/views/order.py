import calendar
from datetime import datetime
from app.calendar.forms import EventForm
from core.utils import get_content_type_for_model
from django.shortcuts import render, get_object_or_404, redirect
from app.orders.forms import OrderForm, AddParticipantToOrderForm, CreateInvoiceForm
from app.orders.models import Order, ProductLine, Invoice
from app.stock.models import Product
from core import Core
from core.auth.log.models import Log
from core.auth.permission.models import Permission
from core.decorators import require_permission, login_required
from django.utils.translation import ugettext as _
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType
from core.shortcuts import comment_block
from operator import itemgetter, attrgetter
from util.ordereddict import OrderedDict

@require_permission("LIST", Order)
def my_orders(request):
    orders = Core.current_user().get_permitted_objects("VIEW", Order).filter(trashed=False)

    return render(request, "orders/overview.html", {'title': 'Orders',
                                                    'orders': orders})


@require_permission("VIEW", Order)
def overview(request):
    orders = Order.objects.filter_current_company()
    return render(request, "orders/overview.html", {'title': 'Orders',
                                                    'orders': orders})


@require_permission("VIEW", Order)
def archive(request):
    orders = Order.archived_objects.filter_current_company()

    return render(request, "orders/overview.html", {'title': 'Orders',
                                                    'orders': orders})


@require_permission("VIEW", Order, "id")
def view_hourregistrations(request, id):
    order = Order.objects.filter_current_company().get(id=id)

    stats = OrderedDict()

    for hourregistration in order.hourregistrations.all():
        year_month = (hourregistration.date.year, hourregistration.date.month)

        if not year_month in stats:
            stats[year_month] = OrderedDict()

        if not hourregistration.creator in stats[year_month]:
            stats[year_month][hourregistration.creator] = {'hours': 0, 'hourregistrations': []}

        stats[year_month][hourregistration.creator]['hours'] += hourregistration.hours

        stats[year_month][hourregistration.creator]['hourregistrations'].append(hourregistration)
        stats[year_month][hourregistration.creator]['hourregistrations'] = sorted(
            stats[year_month][hourregistration.creator]['hourregistrations'], reverse=True, key=attrgetter("date"))

    return render(request, "orders/hourregistrations.html", {'title': order.title,
                                                             'stats': stats,
                                                             'order': order})


@require_permission("EDIT", Order, "id")
def history(request, id):
    instance = get_object_or_404(Order, id=id, deleted=False)

    history = Log.objects.filter(content_type=get_content_type_for_model(instance),
                                 object_id=instance.id)

    return render(request, 'orders/log.html', {'title': _("Latest events"),
                                               'order': instance,
                                               'logs': history[::-1][0:150]})


@require_permission("VIEW", Order, "id")
def view(request, id):
    order = Order.objects.filter_current_company().get(id=id)
    comments = comment_block(request, order)
    who_can_see_this = order.who_has_permission_to('view')

    return render(request, "orders/view.html", {'title': order.title,
                                                'order': order,
                                                'comments': comments,
                                                'who_can_see_this': who_can_see_this})


@require_permission("VIEW", Order, "id")
def preview_order_html(request, id):
    order = Order.objects.filter_current_company().get(id=id)
    return render(request, "orders/pdf.html", {'order': order})


@require_permission("VIEW", Order, "id")
def create_invoice(request, id):
    order = Order.objects.filter_current_company().get(id=id)

    if request.method == "POST":
        form = CreateInvoiceForm(request.POST)

        if form.is_valid():
            #Create order based on offer
            invoice_number = request.POST['invoice_number']
            invoice = Invoice()
            invoice.invoice_number = invoice_number
            invoice.order_id = order.id
            invoice.copy_from(order)

            #Archive the offer
            order.archived = True
            order.save()

            return redirect('app.invoices.views.view', invoice.id)

    else:
        form = CreateInvoiceForm()

    return render(request, "orders/create_invoice.html", {'title': order.title,
                                                          'order': order,
                                                          'next_invoice_number': Invoice.calculate_next_invoice_number()
        ,
                                                          'form': form})


@require_permission("VIEW", Order)
def add(request):
    return form(request)


@require_permission("EDIT", Order, "id")
def edit(request, id):
    return form(request, id)


@login_required()
def form(request, id=None):
    products = []

    if id:
        instance = get_object_or_404(Order, id=id)
        products.extend(instance.product_lines.all())
        order_number = instance.order_number
    else:
        instance = Order()
        order_number = Order.calculate_next_order_number()

    if request.method == "POST":
        form = OrderForm(request.POST, instance=instance)
        products = []

        i = 0
        for p in request.POST.getlist('product_number'):
            p = ProductLine()
            p.description = request.POST.getlist('product_description')[i]
            p.price = request.POST.getlist('product_unit_cost')[i]
            p.count = request.POST.getlist('product_qty')[i]
            p.tax = request.POST.getlist('product_tax')[i]

            try:
                p.product = Product.objects.get(id=int(request.POST.getlist('product_number')[i]))
            except Exception, e:
                p.product = None

            products.append(p)

            i += 1

        if form.is_valid():
            o = form.save(commit=False)
            o.save(no_allemployee_group_permissions=True)
            o.update_products(products)

            request.message_success(_("Successfully saved order"))

            return redirect(view, o.id)
    else:
        form = OrderForm(instance=instance, initial={'order_number': order_number})

    return render(request, "orders/form.html", {'form': form,
                                                'order': instance,
                                                'products': products})


@require_permission("EDIT", Order, "id")
def delete_permission_from_participants(request, id, permission_id):
    try:
        permission = Permission.objects.get(id=permission_id)

        if not permission.user == Core.current_user():
            permission.delete()
            request.message_success("Deleted")
        else:
            request.message_error("You can't delete your own permissions")
    except Exception, e:
        request.message_error("You can't delete this permission")

    return participants(request, id)


@require_permission("EDIT", Order, "id")
def participants(request, id, permission_id=None):
    order = get_object_or_404(Order, id=id)
    content_type = ContentType.objects.get_for_model(Order)

    if permission_id:
        permission = Permission.objects.get(id=permission_id)
    else:
        permission = Permission()

    if request.method == 'POST':
        form = AddParticipantToOrderForm(request.POST)

        if form.is_valid():
            user = form.cleaned_data['user']
            role = form.cleaned_data['role']

            perm = Permission()
            perm.content_type = content_type
            perm.object_id = id
            perm.user = user
            perm.role = role
            perm.save()

            request.message_success(_("Successfully add"))

    add_participant_to_group_form = AddParticipantToOrderForm()

    permissions = Permission.objects.filter(content_type=content_type, object_id=id)

    return render(request, "orders/participants.html", {'form': add_participant_to_group_form,
                                                        'order': order,
                                                        'permissions': permissions})


def get_month_link(param, order, year, month):
    if param == "next":
        if month == 12:
            month = 1
            year += 1
        else:
            month += 1

    else:
        if month == 1:
            month = 12
            year -= 1
        else:
            month -= 1

    return "/orders/order/%s/plan_work/%s/%s/" % (order.id, year, month)

@require_permission("EDIT", Order, "id")
def plan_work(request, id, year=datetime.now().year, month=datetime.now().month):
    order = get_object_or_404(Order, id=id)

    if request.method == "POST":
        form = EventForm(request.POST)

        if form.is_valid():
            event = form.save()

            order.events.add(event)

    form = EventForm()

    cal = {}
    
    users = order.who_has_permission_to("VIEW")

    year = int(year)
    month = int(month)

    days_in_month = calendar.monthrange(year, month)

    for user in users:
        cal[user] = {}

        for day in range(1, days_in_month[1] + 1):
            cal[user][day] = []

        for event in user.events.all():
            for date in event.get_dates():
                if date.year == year and date.month == month:
                    cal[user][date.day].append(event)

    return render(request, "orders/plan_work.html", {'order': order,
                                                     'title': _("Plan work"),
                                                     'form': form,
                                                     'cal': cal,
                                                     'days_in_month': range(1, days_in_month[1] + 1),
                                                     'current_month': (year, month),
                                                     'next_month_link': get_month_link("next", order, year, month),
                                                     'last_month_link': get_month_link("last", order, year, month)
    })


