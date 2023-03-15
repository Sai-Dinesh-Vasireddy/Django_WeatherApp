from django.shortcuts import render,redirect
from .form import CityForm
from .models import City
import requests
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import json
from django.http import HttpResponseRedirect






# Create your views here.

api_key = '2744ca1fd7e64e5db4795e8b2b3d8010'

api_url = 'https://ipgeolocation.abstractapi.com/v1/?api_key=' + api_key


def get_ip_geolocation_data(ip_address):
    response = requests.get(api_url)

    return(response.content)

@login_required(login_url="/")
def home(request):
    url='http://api.openweathermap.org/data/2.5/weather?q={},&appid=7e9c7d83a859763f60c105cc80a12b04&units=metric'
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')


    current_location_json = get_ip_geolocation_data(ip)

    current_location_data = json.loads(current_location_json)

    

    if request.method=='POST':
        form = CityForm(request.POST)
        if form.is_valid():
            NCity = form.cleaned_data['name'].capitalize()
            CCity = City.objects.filter(name=NCity).count()
            if CCity==0:
                res=requests.get(url.format(NCity)).json()
                if res['cod']==200:
                    form.save()
                    messages.success(request," "+NCity+" Added Successfully")
                else:
                    messages.error(request," City Does not Exist ")
            else:
                messages.error(request,"City Already Exists")
        else:
            messages.error(request,"City Already Exists")
        

    form = CityForm()
    cities=City.objects.all()
    data=[]
    current_city = current_location_data['city']
    current_city = current_city.capitalize()
    res = requests.get(url.format(current_city)).json()
    city_weather={
        'city':current_city.capitalize(),
            'temperature' : res['main']['temp'],
            'description' : res['weather'][0]['description'],
            'country' : res['sys']['country'],
            'icon' : res['weather'][0]['icon'],
    }
    data.append(city_weather)
    form = CityForm(request.POST)
    for city in cities:        
        res=requests.get(url.format(city)).json()   
        city_weather={
            'city':city,
            'temperature' : res['main']['temp'],
            'description' : res['weather'][0]['description'],
            'country' : res['sys']['country'],
            'icon' : res['weather'][0]['icon'],
        }
        data.append(city_weather)  
    context={'data' : data,'form':form,'current_city':current_city}
    
    return render(request,"weather.html",context)


def delete_city(request,CName):
    City.objects.get(name=CName).delete()
    messages.success(request," "+CName+" Removed Successfully...!!!")
    return redirect('WeatherInfo')


def login_signup(request):
    if request.method=='POST':
        user_name = request.POST['username']
        passwrd = request.POST['password']
        user = authenticate(request,username=user_name,password=passwrd)
        print(user)
        if user is not None:
            login(request,user) 
            if request.GET.get('next',None):
                return HttpResponseRedirect(request.GET['next'])
            return redirect('WeatherInfo')
        else:
            messages.success(request,('Invalid Credentials'))
            return redirect('login')
        
    return render(request,"login.html")

def logout_user(request):
    logout(request)
    messages.success(request,("logged out successfully"))
    return redirect('login')
    
    