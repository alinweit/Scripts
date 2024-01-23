from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Raeume, MyBookings
from .forms import LoginForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from datetime import datetime, timedelta, date
from calendar import monthcalendar


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
        try:

            user = User.objects.get(username=username)
           
            if check_password(password, user.password):
                
                user = authenticate(request, username=username, password=password)
                auth_login(request, user)

                remember_user = request.COOKIES.get('remember_user', user.email)
                login_status = request.COOKIES.get('login_status', 'True')
                    
                if remember_user:
                    response = redirect('to_homepage')
                    response.set_cookie('remember_user', remember_user, max_age=30)
                    response.set_cookie('login_status', login_status, max_age=30)
                    return response
                
                return redirect('to_homepage')
            
            else:
                messages.error(request, 'Email oder Passwort falsch!')

        except User.DoesNotExist:

            messages.error(request, 'Email oder Passwort falsch!')
                    
        else:
            messages.error(request, 'Email oder Passwort falsch!')
                        
    else:
        form = LoginForm()
        
    return render(request, 'login.html', {'form': form})


def logout(request):
    logout(request)
    return render(request, 'login.html')

#@login_required
def reservation(request):
    return render(request, 'reservation.html')


#@login_required(login_url='login/')
def homepage(request, year, month, day):
    today = datetime.now().date()  
    selected_date = datetime(int(year), int(month), int(day)).date()          
    month_calendar = monthcalendar(year, month)

    bookings =  MyBookings.objects.filter(datum=selected_date).values_list('raumNR_id', flat=True)
    freerooms = Raeume.objects.exclude(raumNR__in=bookings)
    bookings = MyBookings.objects.filter(datum=selected_date).select_related('raumNR')
   	
    context = {
		'today': today,
        'year' : year,
        'month' : month,
        'day' : day,
		'selected_date': selected_date,
		'month_calendar': month_calendar,
        'freerooms': freerooms,
        'bookings' : bookings,
        'users' : request.user
    }
    return render(request, 'homepage.html', context)

#@login_required(login_url='login/')
def to_homepage(request):
    today = datetime.now()

    return redirect ('homepage', year=today.year, month=today.month, day=today.day)

#@login_required
def change_month(request, year, month, day, action):
    today = datetime.now().date()
    selected_date = datetime(int(year), int(month), int(day)) 
            
    if action == 'prev':
            selected_date = selected_date - timedelta(days=day+1)
            if today.month == selected_date.month:
                selected_date = date(selected_date.year, selected_date.month, today.day)
            else:
                selected_date = date(selected_date.year, selected_date.month, 1)
    elif action == 'next':
            selected_date = selected_date + timedelta(days=32)
            if today.month == selected_date.month:
                selected_date = date(selected_date.year, selected_date.month, today.day)
            else:
                selected_date = date(selected_date.year, selected_date.month, 1)
    
    return redirect ('homepage', year=selected_date.year, month=selected_date.month, day=selected_date.day)

#@login_required
def bookings(request):
    today = datetime.now().date()
    
    bookings =  MyBookings.objects.filter(datum__gte=today)

    context = {
        'today': today,
        'bookings' : bookings
        }
    return render(request, 'bookings.html', context)