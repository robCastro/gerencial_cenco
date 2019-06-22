# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect

from datetime import datetime, timedelta
from wkhtmltopdf.views import PDFTemplateView
from django.contrib.auth.decorators import permission_required, login_required
from django.http import Http404, HttpResponse
from apps_cenco.db_app.models import Sucursal
from django.db import connections

## Entradas
def verIngresoEconSuc(request):
	if request.method == 'POST':
		if request.POST.get('previa') == '':
			return verSalidaIngresoEconSuc(request)
		else:
			fechaInicio = request.POST.get('fecha_inicio')
			fechaFin = request.POST.get('fecha_fin')
			return redirect('pdf_ingreso_econ_suc', fechaInicio, fechaFin)
	fechaHoy = datetime.now().date()
	fechaInicio = fechaHoy - timedelta(days = 30)
	context = {
		'fechaHoy' : fechaHoy,
		'fechaInicio' : fechaInicio,
	}
	return render(request, 'supervisor/ingresos-econ-suc.html', context)

def verDesempenioSucursal(request):
	if request.method == 'POST':
		if request.POST.get('previa') == '':
			return verSalidaDesempenioSucursal(request)
		else:
			return redirect('pdf_ingreso_econ_suc', request.POST.get('fecha_inicio'), request.POST.get('fecha_fin'))
	fechaHoy = datetime.now().date()
	fechaInicio = fechaHoy - timedelta(days = 30)
	context = {
		'fechaHoy' : fechaHoy,
		'fechaInicio': fechaInicio,
	}
	return render(request, 'supervisor/desempenio-sucursal.html', context)



## Salidas
def verSalidaIngresoEconSuc(request):
	fechaHoy = datetime.now().date()
	fechaInicio = datetime.strptime(request.POST.get('fecha_inicio'), '%Y-%m-%d')
	fechaFin = datetime.strptime(request.POST.get('fecha_fin'), '%Y-%m-%d')
	sucursales = consultaDetallesDePago(fechaInicio, fechaFin)
	for sucursal in sucursales:
		print sucursal[0]
	context = {
		'fechaHoy' : fechaHoy,
		'fechaInicio': fechaInicio,
		'fechaFin': fechaFin,
		'sucursales': sucursales,
	}
	return render(request, 'supervisor/sal-ingresos-econ-suc.html', context)

def verSalidaDesempenioSucursal(request):
	fechaHoy = datetime.now().date()
	fechaInicio = datetime.strptime(request.POST.get('fecha_inicio'), '%Y-%m-%d')
	fechaFin = datetime.strptime(request.POST.get('fecha_fin'), '%Y-%m-%d')
	sucursales = consultaDesempenioSucursal(fechaInicio, fechaFin)
	context = {
		'fechaHoy' : fechaHoy,
		'fechaInicio': fechaInicio,
		'fechaFin': fechaFin,
		'sucursales': sucursales,
	}
	return render(request, 'supervisor/sal-desempenio-sucursal.html', context)



## Reportes
class RepIngresosEconSucursal(PDFTemplateView):
    filename = 'Reporte_Ingresos_Econ_Suc.pdf'
    template_name = 'supervisor/rep-ingresos-econ-suc.html'
    show_content_in_browser=True ###Para no descargar automaticamente
    ###Para agregar context manuales
    def get_context_data(self, **kwargs):
		context = super(RepIngresosEconSucursal, self).get_context_data(**kwargs)
		fechaInicio = datetime.strptime(self.kwargs['fechaInicio'], '%Y-%m-%d')
		fechaFin = datetime.strptime(self.kwargs['fechaFin'], '%Y-%m-%d')
		context['fechaHoy'] = datetime.now().date()
		context['fechaInicio'] = fechaInicio
		context['fechaFin'] = fechaFin
		context['sucursales'] = consultaDetallesDePago(fechaInicio, fechaFin)
		return context

class RepDesempenioSucursal(PDFTemplateView):
	filename = 'Reporte_Desempenio_Sucursal.pdf'
	template_name = 'supervisor/rep-desempenio-sucursal.html'
	show_content_in_browser = True
	def get_context_data(self, **kwargs):
		context = super(RepDesempenioSucursal, self).get_context_data(**kwargs)
		fechaHoy = datetime.now().date()
		fechaInicio = datetime.strptime(kwargs['fechaInicio'], '%Y-%m-%d')
		fechaFin = datetime.strptime(kwargs['fechaFin'], '%Y-%m-%d')
		context['sucursales'] = consultaDesempenioSucursal(fechaInicio, fechaFin)
		context['fechaInicio'] = fechaInicio
		context['fechaFin'] = fechaFin
		context['fechaHoy'] = fechaHoy
		return context



##Consultas Aux
def consultaDetallesDePago(fechaInicio, fechaFin):
	with connections['default'].cursor() as cursorSG:
		cursorSG.execute("""
			select municipio_sucursal, telefono_sucursal, direccion_sucursal, sum(monto_pago) 
			from db_app_detallepago
			inner join db_app_colegiatura on codigo_colegiatura = colegiatura_id
			inner join db_app_expediente on codigo_expediente = expediente_id
			inner join db_app_alumno al on codigo = alumno_id
			inner join db_app_sucursal su on al.sucursal_id = su.codigo_sucursal
			where cancelado = true and fecha_pago between '{}' and '{}'
			group by municipio_sucursal, telefono_sucursal, direccion_sucursal
		""".format(datetime.strftime(fechaInicio,'%Y-%m-%d'), datetime.strftime(fechaFin, '%Y-%m-%d')))
		return cursorSG.fetchall()

def consultaDesempenioSucursal(fechaInicio, fechaFin):
	with connections['default'].cursor() as cursorSG:
		cursorSG.execute("""
			select municipio_sucursal, telefono_sucursal, direccion_sucursal, round(avg(nota_evaluacion),2)
			from db_app_evaluacion
			inner join db_app_empleado em on em.codigo = profesor_id
			inner join db_app_sucursal on codigo_sucursal = em.sucursal_id
			group by municipio_sucursal, telefono_sucursal, direccion_sucursal
			order by round asc;
		""")
		return cursorSG.fetchall()