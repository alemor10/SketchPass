# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth import authenticate, login,logout
from django.shortcuts import render, redirect
from .forms import LoginForm
from .forms import RegisterForm
from django.http import JsonResponse
from mainApp.models import User

# Create your views here.
def index(request):
	login_form = LoginForm()
	register_form = RegisterForm()

	if request.method == 'POST':
		if 'login-submit' in request.POST:
			login_form = LoginForm(request.POST)
			email = request.POST.get("email_login", None)
			password = request.POST.get("password_login", None)

			if login_form.is_valid():
				user = authenticate(email = email, password = password)

				if user is not None:
				    login(request, user)
				    if request.user.is_staff:
			       		return redirect('/admin/')
				    else:
				       return redirect("home/")
			else:
				return render(request, 'mainApp/index.html', {'login_form' : login_form, 'register_form':register_form, 'state':1})

		elif 'register-submit' in request.POST:
			register_form = RegisterForm(request.POST)
			email = request.POST.get("email_register", None)
			password = request.POST.get("password_register", None)

			if register_form.is_valid():
				register_form.save()
				user = authenticate(email = email, password = password)
				if user is not None: #error checking to make sure inserted correctly
					login(request, user)
					if request.user.is_staff:
						return redirect('/admin/')
					else:
						return redirect("home/")
			else:
				return render(request, 'mainApp/index.html', {'login_form' : login_form, 'register_form':register_form, 'state':2})
	else:
		login_form = LoginForm()
		register_form = RegisterForm()
	return render(request, 'mainApp/index.html', {'login_form' : login_form, 'register_form':register_form, 'state':0})
