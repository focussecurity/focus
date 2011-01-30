# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect, HttpResponseRedirect
from core import Core
from core.models import Log, User

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        redirect_to = request.REQUEST.get('next', '')

        if Core.login(request, username, password):
            user = User.objects.get(username=username)

            if user.canLogin:
                if not redirect_to:
                    return HttpResponseRedirect("/dashboard/")
                return HttpResponseRedirect('%s' % redirect_to)
            Log(message="%s forsøkte å logge inn, men er sperret!" % user).save(user=user)
            return render_to_response('login.html')
        
        else:
            try:
                user = User.objects.get(username=username)
                Log(message="%s forsøkte å logge inn, men brukte feil passord." % user).save(user=user)
            except:
                pass
            
    return render_to_response('login.html')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/accounts/login/")

"""
def login (request):

    # If next page is defined, use that instead of the default
    next = request.GET.get('next', '/')

    # Attempt to log in. If successful, redirect to the next page, if not, show error
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            if Core.login(request, data['username'], data['password'], data['remember']):
                return redirect(next)

            else:
                request.message_error("Feil brukernavn og/eller passord, vennligst prøv igjen, eller be om ny passord :)")

        else:
            request.message_error('Du må fylle ut både brukernavn og passord!')
    else:
        form = LoginForm()

    return render_with_request(request, 'user/login.html', {'login_form': form})
"""

def logout (request):
    Core.logout(request)
    return redirect('/')