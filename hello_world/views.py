# your_app/views.py
from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm

def index(request):
    context = {
        "title": "Django example",
    }
    return render(request, "index.html", context)

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the user after registration
            return redirect('profile')  # Redirect to the user's profile or another page
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})
