from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from .models import User
from django.utils.decorators import method_decorator
from library.decorators import unauthenticated_user


class LoginView(View):
    @method_decorator(unauthenticated_user)
    def get(self, request):
        return render(request, "users/login.html")

    @method_decorator(unauthenticated_user)
    def post(self, request, *args, **kwargs):

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is None:
            return render(request, "users/login.html", {
                "message": "Invalid username and/or password."
            })

        login(request, user)
        return HttpResponseRedirect(reverse("auctions:index"))


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("auctions:index"))


class RegisterView(View):

    @method_decorator(unauthenticated_user)
    def get(self, request):
        return render(request, "users/register.html")

    @method_decorator(unauthenticated_user)
    def post(self, request, *args, **kwargs):

        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "users/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "users/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("auctions:index"))
