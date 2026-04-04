from django.shortcuts import render
from .models import Espacio

def dashboard(request):
    espacios = Espacio.objects.filter(activo=True)
    context = {
        'espacios': espacios,
        'total_espacios': espacios.count(),
    }
    return render(request, 'core/dashboard.html', context)
