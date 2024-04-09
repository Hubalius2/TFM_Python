from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import connection

# Create your views here.


def say_hello(request):
    return HttpResponse('Hello, Django!')

def welcome(request):
    return render(request, 'welcome.html')

def carApp(request):
    return render(request, 'carApp.html')

def oil_car(request):
    raw_query = "SELECT * FROM marcas"
    with connection.cursor() as cursor:
        cursor.execute(raw_query)
        marcas = cursor.fetchall()
    
    raw_query = "SELECT * FROM combustible"
    with connection.cursor() as cursor:
        cursor.execute(raw_query)
        combustible = cursor.fetchall()

    raw_query = "SELECT * FROM provincias"
    with connection.cursor() as cursor:
        cursor.execute(raw_query)
        provincias = cursor.fetchall()

    return render(request, 'oil_car.html', {'marcas': marcas, 'combustible': combustible, 'provincias': provincias})

def load_models(request, car_make_id):
    raw_query = "select DISTINCT m.* from fichas_tecnicas ft inner join modelos m on ft.modelid =m.modelid where ft.makeid = '" + str(car_make_id) + "'"
    with connection.cursor() as cursor:
        cursor.execute(raw_query)
        modelos = cursor.fetchall()
   
    return JsonResponse({'modelos': modelos})

def load_versions(request, car_model_id):
    raw_query = "select DISTINCT v.* from fichas_tecnicas ft inner join versiones v on ft.versionid = v.versionid  where ft.modelid  = '" + str(car_model_id) + "'"
    with connection.cursor() as cursor:
        cursor.execute(raw_query)
        versiones = cursor.fetchall()

    return JsonResponse({'versiones': versiones})