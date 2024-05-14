from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse
from .models import Diseases
import requests
from bs4 import BeautifulSoup
from googletrans import Translator





from googletrans import Translator
from django.shortcuts import render
from django.db.models import Q
from .models import Diseases

def translate_urdu_to_english(text):
    translator = Translator()
    translation = translator.translate(text, src='ur', dest='en')
    return translation.text

def search_diseases(request):
    if request.method == 'POST':
        search_query = request.POST.get('search_query')
        if search_query:
            # Translate the search query from English to Urdu
            translator = Translator()
            translated_query = translator.translate(search_query, src='en', dest='ur').text

            # Translate the Urdu data into English and perform the search
            results = Diseases.objects.filter(
                Q(disease_name__icontains=translated_query) |
                Q(symptoms__icontains=translated_query) |
                Q(precautions__icontains=translated_query)
            ).prefetch_related('doctorinfo_set')

            return render(request, 'index.html', {'recommendations': results})
    return render(request, 'index.html')


def crawl(request):
    if request.method == 'POST':
        disease_name = request.POST.get('disease_name')
        if disease_name:
            # Extract information based on the entered disease name
            data = extract_info(disease_name)

            if data:
                # Display translated data to the user
                translated_info = "\n\n".join([f"{field.capitalize()}: {value}" for field, value in zip(["disease name", "symptoms", "precautions", "prevention methods", "medication"], data)])

                # Save the crawled data into the Diseases model
                disease = Diseases.objects.create(
                    disease_name=data[0],
                    symptoms=data[1],
                    precautions=data[2],
                    prevention_methods=data[3],
                    medication=data[4]
                )

                # Render the crawl.html template with the crawled data
                return render(request, 'crawl.html', {'translated_info': translated_info})
            else:
                return HttpResponse("Failed to fetch data from Wikipedia.")
        else:
            return HttpResponse("Please enter a disease name.")
    else:
        return render(request, 'crawl.html')

# Function to extract information from the Wikipedia page based on the disease name
def extract_info(disease_name):
    try:
        # Construct the URL based on the disease name
        url = "https://en.wikipedia.org/wiki/" + disease_name

        # Fetch the webpage
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract disease name
        disease_name_tag = soup.find('span', {'class': 'mw-page-title-main'})
        if disease_name_tag:
            disease_name = disease_name_tag.text.strip()
        else:
            return None

        # Extract symptoms
        symptoms_tag = soup.find('a', {'title': 'Signs and symptoms'})
        if symptoms_tag:
            symptoms = symptoms_tag.find_next('td', {'class': 'infobox-data'}).text.strip()
        else:
            symptoms = "Symptoms not found."

        # Extract precautions
        precautions_tag = soup.find('th', text='Prevention')
        if precautions_tag:
            precautions = precautions_tag.find_next('td', {'class': 'infobox-data'}).text.strip()
        else:
            precautions = "Precautions not found."

        # Extract prevention methods
        prevention_tag = soup.find('span', {'id': 'Prevention'})
        if prevention_tag:
            prevention_text = prevention_tag.find_next('p').text.strip()
        else:
            prevention_text = "Prevention methods not found."

        # Extract antimalarial medication
        medication_tag = soup.find('a', {'title': 'Medication'})
        if medication_tag:
            medication = medication_tag.find_next('a', {'title': 'Antimalarial medication'}).text.strip()
        else:
            medication = "Antimalarial medication not found."

        # Translate data into Urdu
        translator = Translator()
        disease_name_urdu = translator.translate(disease_name, src='en', dest='ur').text
        symptoms_urdu = translator.translate(symptoms, src='en', dest='ur').text
        precautions_urdu = translator.translate(precautions, src='en', dest='ur').text
        prevention_text_urdu = translator.translate(prevention_text, src='en', dest='ur').text
        medication_urdu = translator.translate(medication, src='en', dest='ur').text

        return (disease_name_urdu, symptoms_urdu, precautions_urdu, prevention_text_urdu, medication_urdu)

    except Exception as e:
        return None

from django.shortcuts import render, redirect
from .models import Doctors
from .forms import DoctorForm

def register_doctor(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('register_doctor')
    else:
        form = DoctorForm()
    return render(request, 'register_doctor.html', {'form': form})

from django.shortcuts import render, redirect
from .models import Doctors

def doctor_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Check if the provided email exists in the Doctors model
        try:
            doctor = Doctors.objects.get(email=email)
        except Doctors.DoesNotExist:
            doctor = None
        
        if doctor is not None and doctor.password == password:
            # Store email in session
            request.session['doctor_email'] = email
            # Redirect to doctor's dashboard or any other page
            return redirect('dashboard')  # Change 'dashboard' to the name of your doctor's dashboard URL
        else:
            # Invalid login, display an error message
            return render(request, 'login.html', {'error': 'Invalid email or password'})
    else:
        return render(request, 'login.html')

from django.shortcuts import render, redirect
from .models import Doctors, Diseases

def doctor_dashboard(request):
    # Get the doctor's email from session
    doctor_email = request.session.get('doctor_email')
    if doctor_email:
        # Fetch the doctor object using the email
        try:
            user = Doctors.objects.get(email=doctor_email)
        except Doctors.DoesNotExist:
            user = None
        if user:
            # Fetch all diseases
            diseases = Diseases.objects.all()
            return render(request, 'dashboard.html', {'user': user, 'diseases': diseases})
    # Redirect to login page if email session variable is not found or doctor not found
    return redirect('doctor_login')

from django.shortcuts import render, redirect
from .models import Diseases, DoctorInfo

from googletrans import Translator

def add_doctor_info(request):
    if request.method == 'GET':
        disease_id = request.GET.get('disease_id')
        if disease_id:
            try:
                disease = Diseases.objects.get(id=disease_id)
            except Diseases.DoesNotExist:
                disease = None
            if disease:
                return render(request, 'add_doctor_info.html', {'disease': disease})
        return redirect('doctor_dashboard')  # Redirect to doctor dashboard if disease ID is not found or invalid
    
    elif request.method == 'POST':
        disease_id = request.POST.get('disease_id')
        doctor_name = request.POST.get('doctor_name')
        doctor_phone = request.POST.get('doctor_phone')
        doctor_advice = request.POST.get('doctor_advice')

        if disease_id and doctor_name and doctor_phone and doctor_advice:
            # Translate doctor's input to Urdu
            translator = Translator()
            doctor_name_urdu = translator.translate(doctor_name, src='en', dest='ur').text
            doctor_advice_urdu = translator.translate(doctor_advice, src='en', dest='ur').text

            # Create and save DoctorInfo object
            DoctorInfo.objects.create(
                disease_id=Diseases.objects.get(id=disease_id),
                doctor_name=doctor_name_urdu,
                doctor_phone=doctor_phone,
                doctor_advice=doctor_advice_urdu
            )
            return redirect('dashboard')  # Redirect to doctor dashboard after saving doctor info
        else:
            # Handle invalid form submission
            return render(request, 'add_doctor_info.html', {'error': 'Invalid form submission'})



from django.shortcuts import redirect
from django.contrib.auth import logout

def doctor_logout(request):
    logout(request)
    # Redirect to the home page or any other page after logout
    return redirect('index')  # Change 'index' to the name of your home page URL
