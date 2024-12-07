from django.shortcuts import render, redirect
from .models import Car
from .forms import CarForm
import csv
import io

def index(request):
    cars = Car.objects.all()
    return render(request, 'csvcrud/index.html', {'cars': cars})

def car_list(request):
    cars = Car.objects.all()
    return render(request, 'csvcrud/product_list.html', {'cars': cars})

def car_create(request):
    if request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('car_list')
    else:
        form = CarForm()
    return render(request, 'csvcrud/car_form.html', {'form': form})

def car_update(request, id):
    car = Car.objects.get(id=id)
    if request.method == 'POST':
        form = CarForm(request.POST, instance=car)
        if form.is_valid():
            form.save()
            return redirect('car_list')
    else:
        form = CarForm(instance=car)
    return render(request, 'csvcrud/car_form_update.html', {'form': form})

def car_delete(request, id):
    car = Car.objects.get(id=id)
    if request.method == 'POST':
        car.delete()
        return redirect('car_list')
    return render(request, 'csvcrud/car_confirm_delete.html', {'car': car})

def import_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv'):
            return render(request, 'csvcrud/import_csv.html', {'error': 'This is not a CSV file'})
        
        # Read CSV file
        data_set = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(data_set)
        next(io_string)
        for column in csv.reader(io_string, delimiter=',', quotechar="|"):
            _, created = Car.objects.update_or_create(
                name=column[0],
                brand=column[1],
                model=column[2],
                price=column[3],
            )
        return redirect('car_list')

    return render(request, 'csvcrud/import_csv.html')
