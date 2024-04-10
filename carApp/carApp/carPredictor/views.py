from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import connection
import pandas as pd
from sklearn.impute import KNNImputer
import pickle
import numpy as np
# Create your views here.

with open('C:/Master/TFM/Code_Python/TFM_Python/carApp/carApp/static/modeling/predictors.pkl', 'rb') as f:
    variables_cargadas = pickle.load(f)

# Asignar las variables cargadas a las variables locales
ventas_oil = variables_cargadas['ventas_oil']
ventas_elec = variables_cargadas['ventas_elec']
best_tuning_oil_set_nd = variables_cargadas['best_tuning_oil_set_nd']
best_tuning_elec_set_nd = variables_cargadas['best_tuning_elec_set_nd']




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

    raw_query = "SELECT * FROM bodytype"
    with connection.cursor() as cursor:
        cursor.execute(raw_query)
        bodytype = cursor.fetchall()

    raw_query = "SELECT * FROM provincias"
    with connection.cursor() as cursor:
        cursor.execute(raw_query)
        provincias = cursor.fetchall()

    return render(request, 'oil_car.html', {'marcas': marcas, 'combustible': combustible, 'provincias': provincias, 'bodytype': bodytype})

def load_models(request, car_make_id, car_year):
    raw_query = "select DISTINCT m.* from fichas_tecnicas ft inner join modelos m on ft.modelid =m.modelid where ft.makeid = '" + str(car_make_id) + "' and ft.vehicleyear = '" + str(car_year) + "'"
    with connection.cursor() as cursor:
        cursor.execute(raw_query)
        modelos = cursor.fetchall()
   
    return JsonResponse({'modelos': modelos})

def load_versions(request, car_model_id, car_make_id, car_year):
    raw_query = "select DISTINCT v.* from fichas_tecnicas ft inner join versiones v on ft.versionid = v.versionid  where ft.makeid = '" + str(car_make_id) + "' and ft.vehicleyear = '" + str(car_year) + "' and ft.modelid  = '" + str(car_model_id) + "'" 
    with connection.cursor() as cursor:
        cursor.execute(raw_query)
        versiones = cursor.fetchall()

    return JsonResponse({'versiones': versiones})

def predict(request):
    car_make = request.POST.get('make')
    car_model = request.POST.get('model')
    car_version = request.POST.get('version')
    car_year = request.POST.get('vehicleyear')
    car_km = request.POST.get('kilometros')
    car_province = request.POST.get('provincia_form')

    
    datos_coche = ventas_oil[(ventas_oil['makeid'] == float(car_make)) & 
                             (ventas_oil['vehicleyear'] == float(car_year)) &
                             (ventas_oil['modelid'] == float(car_model)) &
                             (ventas_oil['versionid'] == float(car_version))]
    

    if(datos_coche.empty):
        datos_coche = ventas_elec[(ventas_elec['makeid'] == float(car_make)) & 
                             (ventas_elec['vehicleyear'] == float(car_year)) &
                             (ventas_elec['modelid'] == float(car_model)) &
                             (ventas_elec['versionid'] == float(car_version))]
        if(datos_coche.empty):
            return JsonResponse({'prediction': 0, 'Precio Compra': 'Ha habido un error en la selección de los datos'})
    
    print(car_make)
    print(car_model)
    print(car_version)
    print(car_year)
    print(datos_coche)
    datos_coche = datos_coche.iloc[0]
    datos_coche['makeid'] = car_make
    datos_coche['vehicleyear'] = car_year
    datos_coche['km'] = car_km
    datos_coche['provinceid'] = car_province
    datos_coche = pd.DataFrame(datos_coche).transpose()
    car_test_features = datos_coche.drop(columns=['price_amount', 'modelid', 'versionid'])
    if(datos_coche['combustible_type_id'].isin([1, 2, 4, 6, 7]).any()):
        car_test_prediction = best_tuning_oil_set_nd.predict(car_test_features)
    else:
        car_test_prediction = best_tuning_elec_set_nd.predict(car_test_features)
    
    car_test_prediction = 10 ** car_test_prediction
    
    raw_query = "select ft.photos, m.model, ma.make, v.version from fichas_tecnicas ft inner join modelos m on ft.modelid = m.modelid inner join marcas ma on ft.makeid = ma.makeid inner join versiones v on ft.versionid = v.versionid where ma.makeid = '" + str(car_make) + "' and m.modelid = '" + str(car_model) + "' and v.versionid = '" + str(car_version) + "' and ft.vehicleyear = '" + str(car_year) + "'"
    with connection.cursor() as cursor:
        cursor.execute(raw_query)
        photo = cursor.fetchall()
    
    return render(request, 'carApp.html', {'prediction': car_test_prediction.item(), 'datos_coche': datos_coche.iloc[0], 'photo': photo})
    

    