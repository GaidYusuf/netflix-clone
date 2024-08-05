from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Movie  # Import the Movie model to query movie data

# Create your views here.


def index(request):
    # Retrieve all movie objects from the database
    movies = Movie.objects.all()

    # Create a context dictionary to pass data to the template
    # The key 'movies' is used to reference the movie data in the template
    context = {
        'movies': movies,
    }

    # Render the 'index.html' template with the context data
    # 'context' contains the data passed to the template
    return render(request, 'index.html', context)


def login(request):
    if request.method == 'POST':
        # Retrieve form data from the POST request
        username = request.POST['username']
        password = request.POST['password']

        # auth.authenticate() checks the provided username and password against the database
        # If the credentials are correct, it returns a User object; otherwise, it returns None
        user = auth.authenticate(username=username, password=password)

        # Check if authentication was successful
        if user is not None:
            # auth.login() saves the user's ID in the session, effectively logging the user in for the current session
            auth.login(request, user)
            # Redirect to the homepage
            return redirect('/')
        else:
            # If authentication fails, display an error message and redirect to the login page
            messages.info(request, 'Credentials Invalid')
            return redirect('login')

    return render(request, 'login.html')


def signup(request):
    # Retrieve form data from the POST request
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']

        # Check if both passwords match
        if password == password2:
            # Check if the email already exists in the database
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email already exists")
                # Redirect to signup page to correct the input
                return redirect('signup')
            # Check if the username already exists in the database
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username already exists')
                return redirect('signup')
            else:
                # Create a new user if email and username are unique
                user = User.objects.create_user(
                    username=username, email=email, password=password)
                user.save()  # Save the user to the database

                # Authenticate the newly created user
                user_login = auth.authenticate(
                    username=username, password=password)
                # Log the user in
                auth.login(request, user_login)
                return redirect('/')
        else:
            # If passwords do not match, show an error message
            messages.info(request, "Passwords do not match")
            return redirect('signup')
    else:
        return render(request, 'signup.html')


def add_to_list():
    pass
