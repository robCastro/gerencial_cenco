# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render

from datetime import datetime

from django.views.generic import DetailView
from wkhtmltopdf.views import PDFTemplateView, PDFTemplateResponse


# Create your views here.


#Entradas
from apps_cenco.db_app.models import Empleado, Grupo, Sucursal


@login_required
def verDesempenioEstudiantil(request):
    if request.user.groups.filter(name="Profesor").exists() or request.user.groups.filter(name="Supervisor").exists():
        if request.user.groups.filter(name="Profesor").exists():
            tipo="prof"
            prof = Empleado.objects.get(username=request.user)
            if request.method == 'POST':
                if 'vistaPrevia' in request.POST:
                    fechaHoy = str((datetime.now().date().strftime("%d/%m/%Y")))
                    grupo=request.POST.get('grupo')
                    desempenio=request.POST.get('desempenio')
                    cantidad=request.POST.get('cantidad')
                    if grupo=='todos':
                        idProf = prof.codigo
                        grupos = Grupo.objects.filter(profesor=idProf, activo_grupo=True).order_by('codigo')
                    else:
                        grupos = Grupo.objects.filter(codigo=grupo).order_by('codigo')
                    context = {
                        'tipo':tipo,
                        'fechaHoy': fechaHoy,
                        'grupos': grupos,
                    }
                    return render(request, 'profesor/sal-desempenio-estudiantil.html',context)
            else:
                 idProf = prof.codigo
                 grupo = Grupo.objects.filter(profesor=idProf, activo_grupo=True)
                 grupos = grupo.order_by('codigo')
                 context = {
                     'tipo': tipo,
                     'grupos': grupos,
                 }
                 return render(request, 'profesor/desempenio-estudiantil.html', context)
        else:
            tipo = "sup"
            if request.method == 'POST':
                if 'vistaPrevia' in request.POST:
                    fechaHoy = str((datetime.now().date().strftime("%d/%m/%Y")))
                    sucursal=request.POST.get('sucursal')
                    grupo=request.POST.get('grupo')
                    desempenio=request.POST.get('desempenio')
                    cantidad=request.POST.get('cantidad')
                    if grupo=='todos':
                        grupos = Grupo.objects.filter(activo_grupo=True).order_by('codigo')
                    else:
                        grupos = Grupo.objects.filter(codigo=grupo).order_by('codigo')
                    context = {
                        'fechaHoy': fechaHoy,
                        'grupos': grupos,
                        'sucursal':sucursal,
                    }
                    return render(request, 'profesor/sal-desempenio-estudiantil.html',context)
            else:
                 sucursales= Sucursal.objects.all().order_by('codigo_sucursal')
                 grupos = Grupo.objects.filter(activo_grupo=True).order_by('codigo')
                 context = {
                     'tipo': tipo,
                     'grupos': grupos,
                     'sucursales':sucursales,
                 }
                 return render(request, 'profesor/desempenio-estudiantil.html', context)
    else:
        raise Http404('Error, no tiene permiso para esta página')


#Salidas


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

