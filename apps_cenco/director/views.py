# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

def verIngresosRetirosEstudiantes(request):
	context = {}
	return render(request, 'director/ingresos-retiros-estudiantes.html', context)
