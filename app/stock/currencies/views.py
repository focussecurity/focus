# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.utils.html import escape
from core.shortcuts import *
from core.decorators import *
from core.views import form_perm, updateTimeout
from app.stock.forms import CurrencyForm
from app.stock.models import Currency

@login_required
def overview(request):
    updateTimeout(request)
    currencies = Currency.objects.for_user()
    return render_with_request(request, 'stock/currencies/list.html', {'title':'Produkter', 'currencies':currencies})

@login_required
def add(request):
    return form(request)

@require_perm('change', Project)
def edit(request, id):
    return form(request, id)

@require_perm('delete', Project)
def delete(request, id):
    Project.objects.get(id=id).delete()
    return redirect(overview)

@login_required
def addPop(request):
    instance = Currency()

    if request.method == "POST":
        form = CurrencyForm(request.POST, instance=instance)

        if form.is_valid():
            o = form.save(commit=False)
            o.owner = request.user
            o.save()
            form.save_m2m()
            return HttpResponse('<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script>' % \
                            ((o._get_pk_val()), (o)))
    else:
        form = CurrencyForm(instance=instance)

    return render_with_request(request, "simpleform.html", {'title':'Valuta', 'form': form })

@login_required
def form (request, id = False):

    if id:
        instance = get_object_or_404(Currency, id = id, deleted=False)
        msg = "Velykket endret valuta"
    else:
        instance = Currency()
        msg = "Velykket lagt til nytt valuta"

    #Save and set to active, require valid form
    if request.method == 'POST':

        form = CurrencyForm(request.POST, instance=instance)
        if form.is_valid():
            o = form.save(commit=False)
            o.owner = request.user
            o.save()
            messages.success(request, msg)

            return redirect(overview)

    else:
        form = CurrencyForm(instance=instance)

    return render_with_request(request, "form.html", {'title':'Valuta', 'form': form })