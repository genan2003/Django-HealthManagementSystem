import datetime

import pandas as pd
import requests
from bs4 import BeautifulSoup
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.db import models
from django.db.models import Count, Q
from django.http import HttpResponseRedirect, JsonResponse, FileResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from reportlab.lib.pagesizes import A4, letter, landscape
from reportlab.pdfgen import canvas
from .forms import RegisterForm, LoginForm, UploadFileForm, AppointmentForm, RescheduleForm, RecomandareForm
from .models import Pacient, Medic, Programare, Recomandare
import io


def get_info_from_medlineplus(request):
    if request.method == 'POST':
        topic = request.POST.get('topic', '')
        # Define the URL of the page to scrape
        url = f"https://medlineplus.gov/{topic}.html"

        # Send a GET request to the server
        response = requests.get(url)

        # If the GET request is successful, the status code will be 200
        if response.status_code == 200:
            # Get the content of the response
            page_content = response.content

            # Create a BeautifulSoup object and specify the parser
            soup = BeautifulSoup(page_content, 'html.parser')

            # Extract the information
            div = soup.find('div', attrs={'id': 'topic-summary'}).text
            # if div is not None:
            #     p = div.find('p')
            #     if p is not None:
            #         info = p.text
            #     else:
            #         info = "No <p> tag found in the <div>."
            # else:
            #     info = "No <div> with the specified class found."
            info = div
            print(info)
            return JsonResponse({'info': info})
        else:
            return "Unable to retrieve information."


def appointment_pdf(request, appointment_id):
    # Get the appointment
    appointment = Programare.objects.get(Id=appointment_id)
    medic = Medic.objects.get(Parafa=appointment.parafa_medic)

    # Create a file-like buffer to receive PDF data
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file"
    p = canvas.Canvas(buffer, pagesize=landscape(letter))
    p.setFont('Helvetica', 16)
    page_width, page_height = landscape(letter)
    text_width = p.stringWidth(f"Appoitment for Dr. {medic.Nume} {medic.Prenume}({medic.Parafa})", "Helvetica", 16)
    x = (page_width - text_width) / 2
    y = page_height - 50
    p.drawString(x, y, f"Appoitment with Dr. {medic.Nume} {medic.Prenume}({medic.Parafa})")
    text_width = p.stringWidth(f"NR.{appointment_id}/{datetime.datetime.now().year}", "Helvetica", 14)
    x1 = (page_width - text_width) / 2
    y1 = page_height - 50
    p.drawString(x1, y1 - 20, f"NO.{appointment_id}/{datetime.datetime.now().year}")
    p.setFont('Helvetica', 14)
    your_text = f"First name and last name of the pacient: {appointment.Pacient.Nume} {appointment.Pacient.Prenume}"
    p.drawString(50, y - 50, your_text)
    your_text = f"CNP of the pacient: {appointment.Pacient.CNP}"
    p.drawString(50, y - 80, your_text)
    your_text = f"Date of the appointment: {appointment.Data}"
    p.drawString(50, y - 110, your_text)
    your_text = f"City of the doctor's office: {medic.oras}"
    p.drawString(50, y - 140, your_text)

    # Close the PDF object cleanly, and end writing process
    p.showPage()
    p.save()

    # Get the value of the BytesIO buffer and set it as the start of the stream
    buffer.seek(0)

    # Create a FileResponse using the BytesIO buffer
    filename = f'appointment_{appointment.Id}.pdf'
    response = FileResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename={filename}'
    return response


def recomandare_pdf(request, programare_id):
    # Get the Programare instance
    programare = Programare.objects.get(Id=programare_id)

    # Check if there is a Recomandare for this Programare
    try:
        recomandare = Recomandare.objects.get(programare=programare)
    except Recomandare.DoesNotExist:
        return HttpResponse('No recommendation found for this appointment.')

    # Create a file-like buffer to receive PDF data
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file"
    p = canvas.Canvas(buffer, pagesize=A4)
    p.setFont('Helvetica', 14)
    page_width, page_height = A4

    text_width = p.stringWidth("Doctor's recommendation", "Helvetica", 14)
    x = (page_width - text_width) / 2
    y = page_height - 50

    p.drawString(x, y, "Doctor's recommendation")
    text_width = p.stringWidth(f"NR.{programare_id}/{datetime.datetime.now().year}", "Helvetica", 14)
    x1 = (page_width - text_width) / 2
    y1 = page_height - 50
    p.drawString(x1, y1 - 20, f"NO.{programare_id}/{datetime.datetime.now().year}")
    p.setFont('Helvetica', 12)
    your_text = f"First name and last name of the pacient: {programare.Pacient.Nume} {programare.Pacient.Prenume}"
    p.drawString(50, y - 50, your_text)
    your_text = f"Cities of residence: {programare.Pacient.oras}"
    p.drawString(50, y - 80, your_text)
    your_text = f"CNP of the pacient: {programare.Pacient.CNP}"
    p.drawString(50, y - 110, your_text)
    your_text = f"Recommandation from the medic: {recomandare.text}"
    p.drawString(50, y - 140, your_text)
    your_text = f"Doctor's signature: {recomandare.medic.Parafa}"
    p.drawString(50, y - 550, your_text)
    your_text = f"Date : {datetime.datetime.now().date()}"
    p.drawString(50, y - 580, your_text)

    p.showPage()
    p.save()

    # Get the value of the BytesIO buffer and write it to the response
    pdf = buffer.getvalue()
    buffer.close()
    return FileResponse(io.BytesIO(pdf), as_attachment=True, filename='recomandare.pdf')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'registerCustom.html', {'form': form})


def home(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            pacient_cnp = form.cleaned_data['CNP']
            request.session['CNP'] = pacient_cnp
            messages.add_message(request, messages.INFO, pacient_cnp, extra_tags='CNP')
            request.session.save()
            user_type = form.cleaned_data.get('user_type')
            CNP = form.cleaned_data.get('CNP')
            password = form.cleaned_data.get('password')

            user = None
            if user_type == 'Pacient':
                try:
                    user = Pacient.objects.get(CNP=CNP)
                except Pacient.DoesNotExist:
                    pass
            else:  # user_type == 'Medic'
                try:
                    user = Medic.objects.get(CNP=CNP)
                    if user.password == password:  # Direct comparison
                        login(request, user)
                        return redirect('medic_home')
                except Medic.DoesNotExist:
                    pass
            if user is not None and user.check_password(password):
                login(request, user)
                if user_type == 'Pacient':
                    return redirect('pacient_home')
                # elif user_type == 'Medic':
                #     return redirect('medic_home')

    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def pacient_home(request):
    cnp = request.session.get('CNP', None)
    user = Pacient.objects.get(CNP=cnp)
    pacient_name = f"{user.Nume} {user.Prenume}"
    top_appointments = Programare.objects.values('parafa_medic').annotate(
        num_appointments=Count('parafa_medic')).order_by('-num_appointments')[:5]

    # Get the corresponding Medic objects
    top_medics_parafa = [item['parafa_medic'] for item in top_appointments]
    top_medics = Medic.objects.filter(Parafa__in=top_medics_parafa)

    return render(request, 'pacient-home.html', {
        'pacient_name': pacient_name,
        'now': timezone.now(),
        'top_medics': top_medics,
    })


def create_programare(request):
    if request.method == 'POST':
        # cnp = request.session.get('CNP', None)
        messages_list = messages.get_messages(request)
        cnp = None  # Initialize cnp to None
        for message in messages_list:
            if 'CNP' in message.tags:
                cnp = message.message
                break
        pacient = Pacient.objects.get(CNP=cnp)
        data = request.POST.get('data')
        permite_reprogramare = request.POST.get('permite_reprogramare')
        descriere = request.POST.get('descriere')

        programare = Programare(
            Pacient=pacient,
            Data=timezone.datetime.strptime(data, "%Y-%m-%dT%H:%M"),
            Permite_reprogramare=bool(permite_reprogramare),
            Descriere=descriere,
            parafa_medic=pacient.Parafa_medic_de_familie
        )
        programare.save()

        return redirect('pacient_home')

    return render(request, 'make-appointment.html')


def programare_list(request):
    # Get the CNP from the session
    cnp = request.session.get('CNP', None)

    # Get the Pacient object for the logged-in user
    pacient = Pacient.objects.get(CNP=cnp)

    # Get all Programare instances for this Pacient
    programari = Programare.objects.filter(Pacient=pacient)

    # Get the Medic details for each Programare
    for programare in programari:
        medic = Medic.objects.get(Parafa=programare.parafa_medic)
        programare.medic_name = medic.Nume
        programare.medic_specializare = medic.specializare

    # Render the 'programare_list.html' template with the programari context
    return render(request, 'programare_list.html', {'programari': programari})


def search_medic(request):
    # Get the search query from the request
    query = request.GET.get('q', '')

    # Search the Medic model
    results = Medic.objects.filter(
        models.Q(Nume__icontains=query) | models.Q(specializare__icontains=query) | models.Q(oras__icontains=query))

    # Render the 'medic_search.html' template with the results context
    return render(request, 'medic_search.html', {'medics': results})


def create_appointment(request, medic_id):
    medic = get_object_or_404(Medic, id=medic_id)
    pacient = get_object_or_404(Pacient, CNP=request.session.get('CNP', None))  # Get the logged-in user

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.Pacient = pacient  # Set the patient to the logged-in user
            appointment.parafa_medic = medic.Parafa
            appointment.save()
            return redirect('pacient_home')  # Redirect to a success page after creating the appointment
    else:
        form = AppointmentForm()

    return render(request, 'make-programare.html', {'form': form, 'medic': medic})


def medic_home(request):
    # Get the logged-in medic
    cnp = request.session.get('CNP', None)
    user = Medic.objects.get(CNP=cnp)

    if request.method == 'POST':
        form = RecomandareForm(request.POST)
        if form.is_valid():
            recomandare = form.save(commit=False)
            recomandare.medic = user
            recomandare.save()
    else:
        form = RecomandareForm()

    # Get all Programare instances for this medic
    programari = Programare.objects.filter(
        Q(parafa_medic=user.Parafa))

    # Render the 'medic_home.html' template with the programari context
    return render(request, 'medic_home.html', {'programari': programari})


def approve_appointment(request, programare_id):
    # Get the Programare instance with the given id
    programare = get_object_or_404(Programare, Id=programare_id)
    cnp = request.session.get('CNP', None)
    user = Medic.objects.get(CNP=cnp)

    # Check if the logged-in user is the medic for this appointment
    if user.Parafa == programare.parafa_medic:
        # Approve the appointment
        programare.aprobat = True
        programare.save()

    # Redirect to the medic's home page
    return redirect('medic_home')


def reschedule_appointment(request, programare_id):
    # Get the Programare instance with the given id
    programare = get_object_or_404(Programare, Id=programare_id)
    cnp = request.session.get('CNP', None)
    user = Medic.objects.get(CNP=cnp)

    # Check if the logged-in user is the medic for this appointment
    if user.Parafa == programare.parafa_medic:
        # Check if rescheduling is allowed for this appointment
        if programare.Permite_reprogramare:
            if request.method == 'POST':
                form = RescheduleForm(request.POST, instance=programare)
                if form.is_valid():
                    form.save()
                    return redirect('medic_home')
            else:
                form = RescheduleForm(instance=programare)
        return render(request, 'reschedule_form.html', {'form': form, 'programare_id': programare_id})

    # Redirect to the medic's home page
    return redirect('medic_home')


def recommandation_create(request, programare_id):
    # Get the Programare instance with the given id
    programare = get_object_or_404(Programare, Id=programare_id)
    cnp = request.session.get('CNP', None)
    user = Medic.objects.get(CNP=cnp)

    # Check if the logged-in user is the medic for this appointment
    if user.Parafa == programare.parafa_medic:
        if request.method == 'POST':
            form = RecomandareForm(request.POST)
            if form.is_valid():
                recomandare = form.save(commit=False)
                recomandare.medic = user
                recomandare.programare = programare  # Set the programare field
                recomandare.save()
                return redirect('medic_home')
        else:
            form = RecomandareForm(initial={'programare': programare})
        return render(request, 'recomandare_create.html', {'form': form})
    return redirect('medic_home')


def logout_view(request):
    logout(request)
    # Redirect to the homepage.
    return HttpResponseRedirect('/')
