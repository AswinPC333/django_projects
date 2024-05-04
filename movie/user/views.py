from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages



from django.contrib.auth.decorators import login_required  
from .models import Movie
from .forms import MovieForm

from django.views.generic import ListView
from .models import Movie


from django.shortcuts import render
from .models import Category



from .forms import MovieForm



from .models import  Review
from .forms import ReviewForm


from django.shortcuts import  get_object_or_404
from .models import Category

def category_movies(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    movies = Movie.objects.filter(category=category)
    return render(request, 'category_movies.html', {'category': category, 'movies': movies})



def search(request):
    query = request.GET.get('q')
    if query:
        movies = Movie.objects.filter(title__icontains=query)
        categories = Category.objects.prefetch_related('movies')
    else:
        movies = []
    return render(request, 'search.html', {'query': query, 'movies': movies,'categories': categories})

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.movie = movie
            review.save()
            return redirect('movie_detail', movie_id=movie_id)
    else:
        form = ReviewForm()
    return render(request, 'movie_detail.html', {'movie': movie, 'form': form})



def edit_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if request.user == movie.user:  # Check if the current user is the one who uploaded the movie
        if request.method == 'POST':
            form = MovieForm(request.POST, request.FILES, instance=movie)
            if form.is_valid():
                form.save()
                return redirect('demo')  # Change this to the URL name of your movie list view
        else:
            form = MovieForm(instance=movie)
        return render(request, 'edit_movie.html', {'form': form})
    else:
        # Return some error or access denied page
        return render(request, 'index.html', {'message': 'You are not authorized to edit this movie.'})



def movie_list(request):
    categories = Category.objects.prefetch_related('movies')
    return render(request, 'home.html', {'categories': categories})


class MovieListView(ListView):
    model = Movie
    template_name = 'movie_list.html'
    paginate_by = 6


@login_required  # Add this decorator
def add_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.user = request.user  # Assign the current user to the movie
            movie.save()
            return redirect('demo')  # Change this to the URL name of your movie list view
    else:
        form = MovieForm()
    return render(request, 'add_movie.html', {'form': form})


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            categories = Category.objects.prefetch_related('movies')
            return render(request, 'home.html', {'user': user,'categories': categories})
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('signin')

    return render(request, "signin.html")

def demo(request):
    if request.user.is_authenticated:
        return render(request, 'home.html', {'user': request.user})
    else:
        return redirect('signin')

def register(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists! Please try a different username.")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect('register')

        if len(username) > 20:
            messages.error(request, "Username must be under 20 characters!")
            return redirect('register')

        if pass1 != pass2:
            messages.error(request, "Passwords didn't match!")
            return redirect('register')

        if not username.isalnum():
            messages.error(request, "Username must be alphanumeric!")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=pass1)
        user.first_name = fname
        user.last_name = lname
        user.save()
        messages.success(request, "Your account has been created successfully!")
        return redirect('signin')

    return render(request, "register.html")

def signout(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('demo')

def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST['fname']
        user.last_name = request.POST['lname']
        user.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('demo')
    else:
        return render(request, 'edit_profile.html', {'user': request.user})

def change_password(request):
    if request.method == 'POST':
        user = request.user
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        if not user.check_password(old_password):
            messages.error(request, "Old password is incorrect!")
            return redirect('change_password')

        if new_password != confirm_password:
            messages.error(request, "New passwords didn't match!")
            return redirect('change_password')

        user.set_password(new_password)
        user.save()
        messages.success(request, "Password changed successfully!")
        return redirect('demo')
    else:
        return render(request, 'change_password.html')
