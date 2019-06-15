# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from datetime import datetime
from wkhtmltopdf.views import PDFTemplateView

# Create your views here.

def verIngresosRetirosEstudiantes(request):
	fechaHoy = str((datetime.now().date().strftime("%m/%d/%Y")))
	#fechaInicio = datetime.strptime(datetime.now().date() - timedelta(days = 7), "%d/%m/%Y").date()
	context = {
		'fechaHoy' : fechaHoy,
		#'fechaInicio' : fechaInicio,
	}
	return render(request, 'director/ingresos-retiros-estudiantes.html', context)

def verDesempenioDidactico(request):
	fechaHoy = str((datetime.now().date().strftime("%m/%d/%Y")))
	context = {
		'fechaHoy' : fechaHoy,
	}
	return render(request, 'director/desempenio-didactico.html', context)

def verDesempenioSucursal(request):
	fechaHoy = str((datetime.now().date().strftime("%m/%d/%Y")))
	context = {
		'fechaHoy' : fechaHoy,
	}
	return render(request, 'director/desempenio-sucursal.html', context)

def verIngresoEconSuc(request):
	fechaHoy = str((datetime.now().date().strftime("%m/%d/%Y")))
	context = {
		'fechaHoy' : fechaHoy,
	}
	return render(request, 'director/ingresos-econ-suc.html', context)



#Salidas


def verSalidaIngresosRetirosEstudiantes(request):
	fechaHoy = str((datetime.now().date().strftime("%m/%d/%Y")))
	#fechaInicio = datetime.strptime(datetime.now().date() - timedelta(days = 7), "%d/%m/%Y").date()
	context = {
		'fechaHoy' : fechaHoy,
		#'fechaInicio' : fechaInicio,
	}
	return render(request, 'director/sal-ingresos-retiros-estudiantes.html', context)

def verSalidaDesempenioSucursal(request):
	fechaHoy = str((datetime.now().date().strftime("%m/%d/%Y")))
	context = {
		'fechaHoy' : fechaHoy,
	}
	return render(request, 'director/sal-desempenio-sucursal.html', context)

def verSalidaIngresoEconSuc(request):
	fechaHoy = str((datetime.now().date().strftime("%m/%d/%Y")))
	context = {
		'fechaHoy' : fechaHoy,
	}
	return render(request, 'director/sal-ingresos-econ-suc.html', context)


#Reportes

class RepIngresosRetirosEstudiantes(PDFTemplateView):
    filename = 'my_pdf.pdf'
    template_name = 'director/rep-ingresos-retiros-estudiantes.html'
    show_content_in_browser=True ###Para no descargar automaticamente
    
    ###Para agregar context manuales
    def get_context_data(self, **kwargs):
    	context = super(RepIngresosRetirosEstudiantes, self).get_context_data(**kwargs)
    	context['fechaHoy'] = str((datetime.now().date().strftime("%d/%m/%Y")))
    	return context
	
