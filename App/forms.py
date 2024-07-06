from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Pacient, Programare, Recomandare


class RegisterForm(UserCreationForm):
    class Meta:
        model = Pacient
        fields = ['Nume', 'Prenume', 'CNP', 'Parafa_medic_de_familie', 'email', 'oras']


class LoginForm(forms.Form):
    USER_TYPE_CHOICES = [
        ('Pacient', 'Pacient'),
        ('Medic', 'Medic'),
    ]

    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES)
    CNP = forms.CharField(max_length=13)
    password = forms.CharField(widget=forms.PasswordInput)


class UploadFileForm(forms.Form):
    file = forms.FileField()


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Programare
        fields = ['Data', 'Permite_reprogramare', 'Descriere']
        widgets = {
            'Data': forms.DateTimeInput(attrs={'class': 'datetimepicker-input', 'id': 'datetimepicker'},
                                        format='%Y-%m-%d %H:%M'),
        }

    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        self.fields['Data'].input_formats = ['%Y-%m-%d %H:%M']


class RescheduleForm(forms.ModelForm):
    class Meta:
        model = Programare
        fields = ['Data']
        widgets = {
            'Data': forms.DateTimeInput(attrs={'class': 'datetimepicker-input'}),
        }


class RecomandareForm(forms.ModelForm):
    class Meta:
        model = Recomandare
        fields = ['text']
