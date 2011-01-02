from django.http import HttpResponse
from app.announcements.models import Announcement
from app.contacts.models import Contact
from app.customers.models import Customer
from app.orders.models import Order
from app.projects.models import Project
from app.timetracking.models import Timetracking
from forms import *
from core.models import Company, Group, Log, Notification
from core.shortcuts import *
from core.decorators import *
from core.views import updateTimeout

@require_permission("LIST", Company)
def overview(request):
    updateTimeout(request)
    companies = Company.objects.all()

    return render_with_request(request, 'company/list.html', {'title': 'Firmaer',
                                                              'companies': companies})

@require_permission("CREATE", Company)
def add(request):
    return newForm(request)

@require_permission("EDIT", Company, 'id')
def edit(request, id):
    return form(request, id)

@login_required()
def form (request, id=False):
    if id:
        instance = Company.objects.all().get(id=id)
        msg = "Velykket endret kunde"
    else:
        instance = Company()
        msg = "Velykket lagt til ny kunde"

    #Save and set to active, require valid form
    if request.method == 'POST':
        form = CompanyForm(request.POST, instance=instance)
        if form.is_valid():
            o = form.save(commit=False)
            o.owner = request.user
            o.save()
            form.save_m2m()
            request.message_success(msg)

            return redirect(overview)
    else:
        form = CompanyForm(instance=instance)

    return render_with_request(request, "form.html", {'title': 'Kunde', 'form': form})

def newForm(request):
    if request.method == 'POST': # If the form has been submitted...
        form = newCompanyForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            name = form.cleaned_data['name']
            adminGroup = form.cleaned_data['adminGroup']
            allEmployeesGroup = form.cleaned_data['allEmployeesGroup']
            adminuserName = form.cleaned_data['adminuserName']
            adminuserUsername = form.cleaned_data['adminuserUsername']
            adminuserPassword = form.cleaned_data['adminuserPassword']

            adminGroup = Group(name=adminGroup)
            adminGroup.saveWithoutCreatePermissions()

            allEmployeesGroup = Group(name=allEmployeesGroup)
            allEmployeesGroup.saveWithoutCreatePermissions()

            company = Company(name=name, adminGroup=adminGroup, allEmployeesGroup=allEmployeesGroup)
            company.save()

            #Create the admin user
            user = User(first_name=adminuserName, username=adminuserUsername)
            user.set_password(adminuserPassword)
            user.company = company
            user.save()

            #Manually give permission to the admin group

            adminGroup.grant_permissions("ALL", adminGroup)
            adminGroup.grant_permissions("ALL", allEmployeesGroup)

            #Add admin user to admin group
            adminGroup.addMember(user)

            #Set the company fields on groups
            adminGroup.company = company
            adminGroup.save()
            allEmployeesGroup.company = company
            allEmployeesGroup.save()

            #Give admin group all permissions on classes
            adminGroup.grant_role("Admin", Project)
            adminGroup.grant_role("Admin", Customer)
            adminGroup.grant_role("Admin", Contact)
            adminGroup.grant_role("Admin", Order)
            adminGroup.grant_role("Admin", Timetracking)
            adminGroup.grant_role("Admin", Announcement)
            adminGroup.grant_role("Admin", Log)
            adminGroup.grant_role("Admin", Notification)
            adminGroup.grant_role("Admin", User)
            adminGroup.grant_role("Admin", Group)
            adminGroup.grant_permissions("CONFIGURE", Company)

            #Give employee group some permissions on classes
            allEmployeesGroup.grant_role("Member", Project)
            allEmployeesGroup.grant_role("Member", Customer)
            allEmployeesGroup.grant_role("Member", Contact)
            allEmployeesGroup.grant_role("Member", Timetracking)
            allEmployeesGroup.grant_role("Member", Order)
            allEmployeesGroup.grant_role("Member", Announcement)
            allEmployeesGroup.grant_role("Member", Log)
            allEmployeesGroup.grant_role("Member", Notification)


            return redirect(overview)
    else:
        form = newCompanyForm() # An unbound form

    return render_with_request(request, "form.html", {'title': 'Nytt firma', 'form': form})
