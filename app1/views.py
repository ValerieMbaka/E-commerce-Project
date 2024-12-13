from django.shortcuts import render
from .models import Slider, AboutSection, Service

# Create your views here.
def index(request):
        # Get all carousel items
        sliders = Slider.objects.all()
        
        # Get only the About section
        about_section = AboutSection.objects.first()
        
        # Fetch all services from the database
        services = Service.objects.all()
        return render(request, 'app1/index.html',
                      {'sliders': sliders,
                       'about_section': about_section,
                       'services': services})