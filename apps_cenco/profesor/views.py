# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required, permission_required
from django.http import Http404
from django.shortcuts import render, redirect

from datetime import datetime, timedelta

from wkhtmltopdf.views import PDFTemplateView
from apps_cenco.db_app.models import Empleado, Grupo

# Create your views here.

#Entradas

@login_required
def verDesempenioEstudiantil(request):
    if request.user.groups.filter(name="Profesor").exists():
        prof = Empleado.objects.get(username=request.user)
        if request.method == 'POST':
            if 'vistaPrevia' in request.POST:
                return verSalidaDesempenioEstudiantil(request)
            if 'descargar' in request.POST:
                fechaHoy = str((datetime.now().date().strftime("%d/%m/%Y")))
                grupo = int(request.POST.get('grupo'))
                desempenio = request.POST.get('desempenio')
                cantidad = request.POST.get('cantidad')
                return redirect('pdf_desempenio_estudiantil', grupo)
        else:
            idProf = prof.codigo
            grupo = Grupo.objects.filter(profesor=idProf, activo_grupo=True)
            grupos = grupo.order_by('codigo')
            context = {
                'grupos': grupos,
            }
            return render(request, 'profesor/desempenio-estudiantil.html', context)
    else:
        raise Http404('Error, no tiene permiso para esta página')

@login_required
def verInasistenciaEstudiantil(request):
    if request.user.groups.filter(name="Profesor").exists():
        prof = Empleado.objects.get(username=request.user)
        if request.method == 'POST':
            if 'vistaPrevia' in request.POST:
                return verSalidaInasistenciaEstudiantil(request)
            if 'descargar' in request.POST:
                fechaHoy = str((datetime.now().date().strftime("%d/%m/%Y")))
                grupo = int(request.POST.get('grupo'))
                cantidad = request.POST.get('cantidad')
                fechaInicio = request.POST.get('fecha_inicio')
                fechaFin = request.POST.get('fecha_fin')
                return redirect('pdf_desempenio_estudiantil', grupo)
        else:
            idProf = prof.codigo
            grupo = Grupo.objects.filter(profesor=idProf, activo_grupo=True)
            grupos = grupo.order_by('codigo')
            fechaHoy = datetime.now().date()
            fechaInicio = fechaHoy - timedelta(days=30)
            context = {
                'grupos': grupos,
                'fechaHoy': str(fechaHoy),
                'fechaInicio': str(fechaInicio),
            }
            return render(request, 'profesor/inasistencia-estudiantil.html', context)
    else:
        raise Http404('Error, no tiene permiso para esta página')


#Salidas
def verSalidaDesempenioEstudiantil(request):
    prof = Empleado.objects.get(username=request.user)
    if request.method == 'POST':
        fechaHoy = str((datetime.now().date().strftime("%d/%m/%Y")))
        grupo = int(request.POST.get('grupo'))
        desempenio = request.POST.get('desempenio')
        cantidad = request.POST.get('cantidad')
        if grupo == 0:
            idProf = prof.codigo
            grupos = Grupo.objects.filter(profesor=idProf, activo_grupo=True).order_by('codigo')
        else:
            grupos = Grupo.objects.filter(codigo=grupo).order_by('codigo')
        context = {
            'grupo': grupo,
            'fechaHoy': fechaHoy,
            'grupos': grupos,
        }
        return render(request, 'profesor/sal-desempenio-estudiantil.html', context)

def verSalidaInasistenciaEstudiantil(request):
    prof = Empleado.objects.get(username=request.user)
    if request.method == 'POST':
        fechaHoy = str((datetime.now().date().strftime("%d/%m/%Y")))
        grupo = int(request.POST.get('grupo'))
        cantidad = request.POST.get('cantidad')
        fechaInicio = request.POST.get('fecha_inicio')
        fechaFin = request.POST.get('fecha_fin')
        if grupo == 0:
            idProf = prof.codigo
            grupos = Grupo.objects.filter(profesor=idProf, activo_grupo=True).order_by('codigo')
        else:
            grupos = Grupo.objects.filter(codigo=grupo).order_by('codigo')
        context = {
            'grupo': grupo,
            'fechaHoy': fechaHoy,
            'grupos': grupos,
            'fechaInicio':datetime.strptime(fechaInicio,"%Y-%m-%d"),
            'fechaFin': datetime.strptime(fechaFin,"%Y-%m-%d"),
        }
        return render(request, 'profesor/sal-inasistencia-estudiantil.html', context)


#Reportes
class RepDesempenioEstudiantil(PDFTemplateView):
    filename = 'desempenio_estudiantil.pdf'
    template_name = 'profesor/rep-desempenio-estudiantil.html'
    show_content_in_browser = True  ###Para no descargar automaticamente

    ###Para agregar context manuales
    def get_context_data(self, **kwargs):
        context = super(RepDesempenioEstudiantil, self).get_context_data(**kwargs)
        context['fechaHoy'] = str((datetime.now().date().strftime("%d/%m/%Y")))
        grupo= int(self.kwargs['grupo'])
        prof = Empleado.objects.get(username=self.request.user)
        if grupo == 0:
            idProf = prof.codigo
            grupos = Grupo.objects.filter(profesor=idProf, activo_grupo=True).order_by('codigo')
        else:
            grupos = Grupo.objects.filter(codigo=grupo).order_by('codigo')
        context['grupos'] = grupos
        return context