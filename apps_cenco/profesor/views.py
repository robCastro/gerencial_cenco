# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from datetime import datetime

from django.views.generic import DetailView
from wkhtmltopdf.views import PDFTemplateView, PDFTemplateResponse


# Create your views here.


#Entradas

def verDesempenioEstudiantil(request):
	return render(request, 'profesor/desempenio-estudiantil.html')


#Salidas

def verSalDesempenioEstudiantil(request):
	fechaHoy = str((datetime.now().date().strftime("%d/%m/%Y")))
	context = {
		'fechaHoy' : fechaHoy,
	}
	return render(request, 'profesor/sal-desempenio-estudiantil.html', context)


#Reportes

class RepDesempenioEstudiantil(PDFTemplateView):
    filename = 'my_pdf.pdf'
    template_name = 'profesor/rep-desempenio-estudiantil.html'
    show_content_in_browser = True  ###Para no descargar automaticamente

    ###Para agregar context manuales
    def get_context_data(self, **kwargs):
        context = super(RepDesempenioEstudiantil, self).get_context_data(**kwargs)
        context['fechaHoy'] = str((datetime.now().date().strftime("%d/%m/%Y")))
        return context

