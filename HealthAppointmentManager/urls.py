from django.urls import path
from App import views
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('pacient/', views.pacient_home, name='pacient_home'),
    path('medic/', views.medic_home, name='medic_home'),
    path('logout/', views.logout_view, name='logout'),
    path('create_programare/', views.create_programare, name='create_programare'),
    path('programare_list/', views.programare_list, name='programare_list'),
    path('search_medic/', views.search_medic, name='search_medic'),
    path('create_appointment/<int:medic_id>/', views.create_appointment, name='create_appointment'),
    path('approve_appointment/<int:programare_id>/', views.approve_appointment, name='approve_appointment'),
    path('reschedule_appointment/<int:programare_id>/', views.reschedule_appointment, name='reschedule_appointment'),
    path('appointment_pdf/<int:appointment_id>/', views.appointment_pdf, name='appointment_pdf'),
    path('recommandation_create/<int:programare_id>/', views.recommandation_create, name='recommandation_create'),
    path('recomandare_pdf/<int:programare_id>/', views.recomandare_pdf, name='recomandare_pdf'),
    path('get_info_from_medlineplus/', views.get_info_from_medlineplus, name='get_info_from_medlineplus'),

]
