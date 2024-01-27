from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Raeume, MyBookings
from .forms import LoginForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User, Group
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
            remember_user = request.POST.get('remember_user', False)
            
            try:
                user = authenticate(request, username=username, password=password)
                            
                if user is not None and check_password(password, user.password):
                    
                    if remember_user:
                        response = redirect('to_homepage')
                        response.set_cookie('remember_user', user.email, max_age=30 * 24 * 60 * 60)
                        response.set_cookie('login_status', 'True', max_age=30 * 24 * 60 * 60)
                        return response
                    
                    auth_login(request, user) 
                    return redirect ('to_homepage')
                        
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
    response = redirect('login')
    
    if request.COOKIES.get('login_status') == 'True':
        response.set_cookie('login_status', 'False', max_age=30 * 24 * 60 * 60)
    logout(request)

    return response

@login_required
def reservation(request):
    return render(request, 'reservation.html')


@login_required
def homepage(request, year, month, day):
    today = datetime.now().date()  
    selected_date = datetime(int(year), int(month), int(day)).date()          
    month_calendar = monthcalendar(year, month)


#Erstellt eine Liste mit Rauemen, welche an dem ausgewählten Tag gebucht sind.
    bookings =  MyBookings.objects.filter(datum=selected_date).values_list('raumNR_id', flat=True)
#Nimmt die gebuchten Raueme aus der Liste der verfügbaren Räume
    freerooms = Raeume.objects.exclude(raumNR__in=bookings)

# Übergibt die Rolle des Users in die Variable "role"
    user = request.user
    groups = Group.objects.filter(user=user)
    role = [group.name for group in groups]

    if role == ['user']:
        bookings = MyBookings.objects.filter(userID=user.id, datum=selected_date)
    else:
        bookings = MyBookings.objects.filter(datum=selected_date)

    context = {
		'today': today,
        'year' : year,
        'month' : month,
        'day' : day,
		'selected_date': selected_date,
		'month_calendar': month_calendar,
        'freerooms': freerooms,
        'bookings' : bookings,
        'role': role,
        'users' : user    
    }
    return render(request, 'homepage.html', context)

@login_required
def to_homepage(request):
    today = datetime.now()

    return redirect ('homepage', year=today.year, month=today.month, day=today.day)

@login_required
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

@login_required
def bookings(request):
    today = datetime.now().date()

    user = request.user
    groups = Group.objects.filter(user=user)
    role = [group.name for group in groups]    
    if role == ['user']:
        bookings = MyBookings.objects.filter(userID=user.id, datum__gte=today)
    else:       
        bookings =  MyBookings.objects.filter(datum__gte=today)

    context = {
        'today': today,
        'bookings' : bookings,
        }
    return render(request, 'bookings.html', context)