from django.shortcuts import render
from django.http import JsonResponse
from .models import Service, Quote


def home(request):
    services = Service.objects.all()
    return render(request, 'solutions/business_solutions.html', {
        'services': services
    })


def save_quote(request):
    if request.method == 'POST':
        service = request.POST.get('service')
        name = request.POST.get('name')
        details = request.POST.get('details')

        Quote.objects.create(
            service=service,
            name=name,
            details=details
        )

        return JsonResponse({'message': 'Quote saved successfully'})