import requests
from django.shortcuts import render,redirect
from . models import City
from .forms import CityForm

# Create your views here.

def index(request):
    url='http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=e95c4343bce13d92bdf94a9e44e698fb'
    cities=City.objects.all()
    weather_data=[]
    err_msg=''
    message=''
    message_class=''

    if request.method=='POST':
        form=CityForm(request.POST)

        if form.is_valid():
            new_city=form.cleaned_data['name']
            existing_city=City.objects.filter(name=new_city).count()

            if existing_city==0:
                r=requests.get(url.format(new_city)).json()
                if r['cod']==200:
                    form.save()
                else:
                    err_msg='City does not exist'
            else:
                err_msg='City already exists'

        if err_msg:
            message=err_msg
            message_class='alert-danger'
        else:
            message='City added successfully'
            message_class='alert-success'
    else:
        form=CityForm()
    
    for city in cities:
        r=requests.get(url.format(city)).json()
        #print(r.text)
       

        city_weather={
            'city': city.name ,
            'temp': r['main']['temp'] ,
            'desc': r['weather'][0]['description'] ,
            'img': r['weather'][0]['icon'] ,
        }
        weather_data.append(city_weather)
        
    context={'weather_data':weather_data,'form':form,'message':message,'message_class':message_class}

    return render(request,'weather.html',context)

def delete(request,city_name):
    City.objects.get(name=city_name).delete()
    return redirect('index')