from app.customers.models import Customer
from app.projects.models import Project
from app.contacts.models import Contact
from core.decorators import login_required
from core.shortcuts import render_with_request
from app.orders.models import Order
from app.suppliers.models import Supplier
from app.stock.models import Product
from app.announcements.models import Announcement

@login_required()
def search(request):
    term = request.GET.get('s')

    searchIn = {}

    searchIn[Customer] = ["full_name", 'email', 'address', 'phone']
    searchIn[Project] = ["project_name", 'pid', 'responsible__first_name']
    searchIn[Contact] = ["full_name", "email", 'address', 'phone']
    searchIn[Order] = ["order_name", "customer__full_name", 'project__project_name', 'description']
    searchIn[Supplier] = ["name"]
    searchIn[Product] = ['name', 'description', 'productGroup__name']
    searchIn[Announcement] = ["title", "text"]

    result = {}

    for o in searchIn.keys():
        for i in searchIn[o]:
            kwargs = {'%s__%s' % ('%s' % i, 'icontains'): '%s' % term}
            k = o.objects.all().filter(**kwargs)

            for s in k:
                if s in result:
                    result[s] += 1
                else:
                    result[s] = 1

    result = sorted(result.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
    v = []
    for i in result:
        v.append(i[0])

    return render_with_request(request, 'search/list.html', {'title': 'Resultat',
                                                             'objects': v})