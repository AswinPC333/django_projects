from django.urls import path
from . import views

urlpatterns = [
    path('', views.movie_list, name='demo'),
    path('signin/', views.signin, name='signin'),
    path('register/', views.register, name='register'),
    path('signout/', views.signout, name='signout'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('add_movie/', views.add_movie, name='add_movie'),
    path('edit_movie/<int:movie_id>/', views.edit_movie, name='edit_movie'),
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('search/', views.search, name='search'),
    path('category/<int:category_id>/', views.category_movies, name='category_movies'),
]

