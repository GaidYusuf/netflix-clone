from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages

# Create your views here.


def index(request):
    return render(request, 'index.html')


def login(request):
    return render(request, 'login.html')


def signup(request):
    # retrieve form data from the POST request
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']

        # Check if both passwords match
        if password == password2:
            # Check if the email already exists in the database
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email already exists.")
                return redirect('signup')  # Redirect to signup page to correct the input
            # Check if the username already exists in the database
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username already exists.')
                return redirect('signup')
            else:
                # Create a new user if email and username are unique
                user = User.objects.create_user(
                    username=username, email=email, password=password)
                user.save() # Save the user to the database

                # Authenticate the newly created user
                user_login = auth.authenticate(
                    username=username, password=password)
                # Log the user in
                auth.login(request, user_login)
                return redirect('/')
        else:
            # If passwords do not match, show an error message
            messages.info(request, "Passwords do not match.")
            return redirect('signup')
    else:
        return render(request, 'signup.html')


def add_to_list():
    pass
