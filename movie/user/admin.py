from django.contrib import admin
from .models import Movie, Category,Review

# Register your models here.
admin.site.register(Category)

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date', 'category', 'user')
    list_filter = ('category', 'user')
    search_fields = ('title', 'description', 'actors')
    date_hierarchy = 'release_date'
    

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('movie', 'user', 'rating', 'comment')
    list_filter = ('movie', 'user')
