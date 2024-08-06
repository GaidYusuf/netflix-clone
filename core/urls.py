from django.urls import path
from . import views

# basic syntax for 'path' function -> path(route, view, name=None)
# route: string representing the URL pattern, 
# view: view function that will handle requests matching this URL pattern, 
# name: (Optional) A name for the URL pattern, which allows you to refer to this URL pattern in other parts of your code, like templates and redirects
urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('logout', views.logout, name='logout'),
    path('movie/<str:pk>', views.movie, name='movie'),
    path('my_list', views.my_list, name='my_list'),
    path('add-to-list/', views.add_to_list, name='add-to-list')
    ]

