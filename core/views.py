# myapp/views.py
import json
import random

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import InvitationForm, RegistrationForm
from core.models import *

## no need to use it since we do not do online delpoyment.
def login_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get("username")
            password = data.get("password")

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return JsonResponse({"status": "successful"})
            else:
                existing_user = authenticate(username=username)

                if existing_user is not None:
                    return JsonResponse({"status": "password_error"})
                else:
                    return JsonResponse({"status": "user_not_found"})

        except Exception as e:
            # Log or print the exception for debugging
            print(f"Exception during login: {str(e)}")
            return JsonResponse({"status": "error", "message": "An error occurred during login"})
    else:
        return JsonResponse({"status": "method_not_allowed"})


def register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except:
            return JsonResponse({"status": "json load fail"})
        invitation_code = data.get("invitation_code")

        try:
            invitation = Invitation.objects.get(code=invitation_code, is_used=False)
        except Invitation.DoesNotExist:
            messages.error(request, 'Invalid invitation code.')
            return JsonResponse({"status": "invalid invitation code"})
        temp = {"username": data.get("username"), "email": data.get("email"), "password1": data.get("password1"),
                "password2": data.get("password2")}
        print(temp)
        form = RegistrationForm(temp)

        if form.is_valid():
            user = form.save()
            invitation.is_used = True
            invitation.save()
            login(request, user)
            messages.success(request, 'Registration successful.')
            return JsonResponse({"status": "successful"})
        else:
            return JsonResponse({"status": "registration form fail", "error": str(form.errors)})
    else:
        form = RegistrationForm()

    return JsonResponse({"status": "fail"})


def generate_invitation_code():
    return random.randint(10 ** 13, 10 ** 14 - 1)


def send_invitation(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except:
            return JsonResponse({"status": "json load fail"})

        inviter_username = data.get("username")
        inviter_password = data.get("password")

        # Authenticate the inviter
        inviter = authenticate(request, username=inviter_username, password=inviter_password)

        if inviter is not None:
            # Inviter is a valid user
            form = InvitationForm({"email": data.get("invited_email")})
        else:
            return JsonResponse({"status": "fail", "error": "illegal inviter"})

        if form.is_valid():
            invitation = form.save(commit=False)
            invitation.code = generate_invitation_code()  # Implement this function
            invitation.save()
            messages.success(request, 'Invitation sent successfully.')
            return JsonResponse({"status": "successful", "code": invitation.code})
        else:
            return JsonResponse({"status": "registration form fail", "error": str(form.errors)})
    else:
        form = InvitationForm()

    return JsonResponse({"status": "fail"})
