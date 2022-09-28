from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .decorators import admin_only, allowed_users, unauthenticated_user
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import Group

# @login_required(login_url="login")
@allowed_users(allowed_roles=["page1"])
def home(request):
	users = User.objects.all().exclude(username=request.user.username)
	context = {
		"users": users,
	}
	return render(request, "index.html", context)

# @unauthenticated_user
@allowed_users(allowed_roles=["customer"])
def customer_page(request):
	context = {
		"message": "I am customer"
	}
	return render(request, "customer_page.html", context)

@allowed_users(allowed_roles=["page1"])
def page1(request):
	context = {
		"message": "I can only view page1"
	}
	return render(request, "page1.html", context)

@allowed_users(allowed_roles=["page2"])
def page2(request):
	context = {
		"message": "I can only view page2"
	}
	return render(request, "page2.html", context)


@allowed_users(allowed_roles=["manager"])
def manager_page(request):
	context = {
		"message": "I am manager"
	}
	return render(request, "manager.html", context)


@allowed_users(allowed_roles=["admin"])
def admin_page(request):
	context = {
		"message": "I am admin"
	}
	return render(request, "admin.html", context)

@admin_only
def add_new_group(request):
	if request.method == "POST":
		name = request.POST.get('name')
		Group.objects.create(name=name)
		messages.success(request, "group added successfully")
		return redirect('home')
	return render(request, "add_group.html")

@admin_only
@require_http_methods(['GET'])
def approve_user_account(request, user_id):
	user = User.objects.get(id=user_id)
	user.is_active = True
	user.save()
	messages.success(request, "User approved")
	return redirect('home')