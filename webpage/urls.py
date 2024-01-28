from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name="login"),
    path('homepage/', views.to_homepage, name="to_homepage"),
    path('homepage/<int:year>-<int:month>-<int:day>/', views.homepage, name="homepage"),
    path('homepage/<int:year>-<int:month>-<int:day>/<str:action>', views.change_month, name="change_month"),
    path('bookings/', views.bookings, name = "bookings"),
    path('remove_bookings/<str:listToDelete>/', views.remove_bookings, name='remove_bookings'),
    path('reservation/', views.reservation, name = "reservation"),
    path('make_booking/<str:data>/', views.make_booking, name="make_booking"),
    path('logout/', views.logout, name = "logout"),
]