from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Movie, MovieList  # Import the Movie model to query movie data
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import re

# Create your views here.


@login_required(login_url='login')
def index(request):
    # Retrieve all movie objects from the database
    movies = Movie.objects.all()

    # Create a context dictionary to pass data to the template
    # The key 'movies' is used to reference the movie data in the template
    context = {
        'movies': movies,  # Pass the movies data to the index.html template
    }

    # Render the 'index.html' template with the context data
    # 'context' contains the data passed to the template
    return render(request, 'index.html', context)


# Ensure the user is logged in; redirect to 'login' if not
@login_required(login_url='login')
def movie(request, pk):
    # Get the movie UUID from the URL parameter `pk`
    movie_uuid = pk  
    # Fetch the movie details from the database using the UUID
    movie_details = Movie.objects.get(uu_id=movie_uuid)

    context = {
        'movie_details': movie_details
    }

    return render(request, 'movie.html', context)


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


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')


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

@login_required(login_url='login')
def add_to_list(request):
    if request.method == 'POST':
        # Retrieve the movie URL from the POST data
        movie_url = request.POST.get('movie_id')
        
        # Define a regex pattern to match UUID format
        uuid_pattern = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
        
        # Search for the UUID in the provided movie URL
        match = re.search(uuid_pattern, movie_url)
        movie_id = match.group() if match else None  # Extract the UUID if a match is found
        
        # Retrieve the Movie object or return a 404 error if not found
        movie = get_object_or_404(Movie, uu_id=movie_id)
        
        # Get or create a MovieList entry for the authenticated user and the movie
        movie_list, created = MovieList.objects.get_or_create(owner_user=request.user, movie=movie)
        
        if created:
            # If the entry was created, return a success message
            response_data = {'status': 'success', 'message': 'Added ✓'}
        else:
            # If the entry already exists, return an informational message
            response_data = {'status': 'info', 'message': 'Movie already in list'}
        
        # Return the response as JSON
        return JsonResponse(response_data)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@login_required(login_url='login')
def my_list(request):
    movie_list = MovieList.objects.filter(owner_user=request.user)
    user_movie_list = []
    
    for movie in movie_list:
        user_movie_list.append(movie.movie)

    context = {
        'movies': user_movie_list
    }
    return render(request, 'my_list.html', context)

@login_required(login_url='login')
def search(request):
    if request.method == 'POST':
        search_term = request.POST['search_term']

        # Filter the Movie objects where the title contains the search term
        #'icontains checks if a field contains a certain substring, ignoring case sensitivity.
        movies = Movie.objects.filter(title__icontains=search_term)

        context = {
            'movies': movies,
            'search_term': search_term,
        }
        return render(request, 'search.html', context)
    else:
        return redirect('/')