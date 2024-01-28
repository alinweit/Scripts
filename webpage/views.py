from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Raeume, MyBookings
from .forms import LoginForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from datetime import datetime, timedelta, date
from calendar import monthcalendar
from django.http import JsonResponse
from django.forms.models import model_to_dict


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
    auth_logout(request)
    response = redirect('login')
    
    if request.COOKIES.get('login_status') == 'True':
        response.set_cookie('login_status', 'False', max_age=30 * 24 * 60 * 60)
    
    return response

@login_required
def reservation(request):
        user = request.user
        groups = Group.objects.filter(user=user)

        if request.method == 'POST':
            selected_date = request.POST.get('datum')   
            selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
            bestuhlung = request.POST.get('bestuhlung')
            ausstattung = request.POST.get('ausstattung')
            if bestuhlung:
                bestuhlung = int(bestuhlung)
            else:
                bestuhlung = 0   

            if selected_date >= datetime.now().date():
                bookings = MyBookings.objects.filter(datum=selected_date).values_list('raumNR_id', flat=True)
                freerooms = Raeume.objects.exclude(raumNR__in=bookings)
                if 'bestuhlung' in request.POST:
                    filtered_freerooms = freerooms.exclude(bestuhlung__lt=bestuhlung)
                    combinations = []
                    for i, room1 in enumerate(freerooms):
                        for room2 in freerooms[i+1:]:
                            if room1 != room2 and (room1.bestuhlung < bestuhlung and room2.bestuhlung < bestuhlung) and (room1.bestuhlung + room2.bestuhlung >= bestuhlung):
                                combinations.append((room1, room2))
                elif 'ausstattung' in request.POST:
                    ausstattung = request.POST.get('ausstattung')
                    if ausstattung == "hoch":
                        filtered_freerooms = freerooms.filter(ausstattung ='hoch')
                    elif ausstattung == "mittel":
                        filtered_freerooms = freerooms.filter(ausstattung='mittel')
                freerooms = filtered_freerooms                     
                context = {
                    'freerooms': freerooms, 
                    'selected_date': selected_date,
                    'user': user,
                    'combinations' : combinations,
                    'bestuhlung' : bestuhlung,
                    'ausstattung' : ausstattung,
                    }       
                    
                return render(request, 'reservation.html', context)                  
            else:
                message = 'Ausgewähltes Datum liegt in der Vergangenheit. Bitte wählen Sie ein anderes Datum aus.'
                context = {
                    'message' : message,
                }
                return render(request, 'reservation.html', context)

        return render(request, 'reservation.html')

@login_required
def make_booking(request, data):
    filtered_data = data.split("|")
    user_id = filtered_data[0]
    raum_nr = filtered_data[1]
    datum = filtered_data[2]
    

    raum = Raeume.objects.get(raumNR=raum_nr)
    user = User.objects.get(username=user_id)
    

    date_obj = datetime.strptime(datum, '%b. %d, %Y')
    formatted_date = date_obj.strftime('%Y-%m-%d')
    

    booking = MyBookings.objects.create(
        userID=user,
        raumNR=raum,
        datum=formatted_date,
    )

    booking_dict = model_to_dict(booking)
    

    return JsonResponse(booking_dict)


@login_required
def homepage(request, year, month, day):
    today = datetime.now().date()  
    selected_date = datetime(int(year), int(month), int(day)).date()          
    month_calendar = monthcalendar(year, month)

    bookings =  MyBookings.objects.filter(datum=selected_date).values_list('raumNR_id', flat=True)

    freerooms = Raeume.objects.exclude(raumNR__in=bookings)

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
        bookings = MyBookings.objects.filter(userID=user.id, datum__gte=today).order_by('datum')
    else:       
        bookings =  MyBookings.objects.filter(datum__gte=today).order_by('datum')

    context = {
        'today': today,
        'bookings' : bookings,
        'role': role,
        }
    return render(request, 'bookings.html', context)

from django.http import JsonResponse

@login_required
def remove_bookings(request, listToDelete):
    bookings_to_delete = listToDelete.split(",")
    for booking_to_delete in bookings_to_delete:
        try:
            MyBookings.objects.filter(pk=booking_to_delete).delete()
            MyBookings.save()
        except:
            None    

    return redirect('bookings')