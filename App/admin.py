from django.urls import path
import pandas as pd
from django.contrib import admin
from django import forms
from django.shortcuts import redirect, render
from import_export.admin import ImportExportModelAdmin
from App.forms import UploadFileForm
from App.models import Pacient, Medic, Programare, Recomandare


@admin.register(Medic)
class ViewAdmin(ImportExportModelAdmin):
    pass


admin.site.register(Pacient)
admin.site.register(Programare)
admin.site.register(Recomandare)
