# views.py
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template
from xhtml2pdf import pisa  # Import ReportLab and xhtml2pdf libraries
from django.http import FileResponse
from reportlab.pdfgen import canvas
from io import BytesIO

from .models import MunicipalProfile, Location, DataReading

def municipal_dashboard(request):
    # Fetch municipal profile information
    municipal_profile = MunicipalProfile.objects.get(user=request.user)  # Assuming you're using authentication

    # Fetch all locations under the municipal profile
    locations = Location.objects.filter(municipal_profile=municipal_profile)

    # Fetch top 5 consumption and top 5 less consumption locations
    top_consumption_locations = DataReading.objects.filter(location__in=locations).order_by('-water_consumption')[:5]
    less_consumption_locations = DataReading.objects.filter(location__in=locations).order_by('water_consumption')[:5]

    # Dummy data for the alert dashboard (you would replace this with your real data)
    alerts = [
        {'location': 'Location A', 'message': 'No water data retrieved'},
        {'location': 'Location B', 'message': 'No electricity data retrieved'},
    ]

    context = {
        'municipal_profile': municipal_profile,
        'locations': locations,
        'top_consumption_locations': top_consumption_locations,
        'less_consumption_locations': less_consumption_locations,
        'alerts': alerts,
    }

    return render(request, 'municipal/dashboard.html', context)

def location_consumption(request, location_id):
    # Fetch the location object
    location = Location.objects.get(id=location_id)

    # Fetch consumption data for electricity and water (customize this based on your data structure)
    electricity_data = DataReading.objects.filter(location=location, electricity_consumption__isnull=False)

    # Fetch water consumption data for a specific location
    water_data = DataReading.objects.filter(location=location, water_consumption__isnull=False)

    context = {
        'location': location,
        'electricity_data': electricity_data,
        'water_data': water_data,
    }

    return render(request, 'municipal/location_consumption.html', context)

# def generate_pdf(request):
#     # Replace this with your actual data retrieval logic
#     location_info = {
#         'name': 'Location XYZ',
#         'latitude': '123.456',
#         'longitude': '789.012',
#         # Add more location details as needed
#     }
#
#     # Render HTML content with location information
#     template = get_template('municipal/location_consumption_pdf.html')  # Create an HTML template
#     context = {'location_info': location_info}
#     html_content = template.render(context)
#
#     # Create a PDF response
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="consumption_report.pdf"'
#
#     # Generate PDF from HTML content
#     pisa_status = pisa.CreatePDF(html_content, dest=response)
#
#     if pisa_status.err:
#         return HttpResponse('PDF generation error')
#
#     return response
#


def generate_pdf(request):
    # Replace this with your actual data retrieval logic
    location_info = {
        'name': 'Location XYZ',
        'latitude': '123.456',
        'longitude': '789.012',
        # Add more location details as needed
    }

    # Create a BytesIO buffer to receive the PDF data
    buffer = BytesIO()

    # Create the PDF object, using the BytesIO buffer as its "file"
    p = canvas.Canvas(buffer)

    # Replace this with your actual PDF content generation logic
    p.drawString(100, 750, "Location Name: " + location_info['name'])
    p.drawString(100, 730, "Latitude: " + location_info['latitude'])
    p.drawString(100, 710, "Longitude: " + location_info['longitude'])
    # Add more information to the PDF as needed

    # Close the PDF object cleanly and finalize the PDF file
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='consumption_report.pdf')
