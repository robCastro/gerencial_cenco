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
@login_required
def verIngresoEconSuc(request):
	if request.user.groups.filter(name="Supervisor").exists():
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
	else:
		raise Http404('Error, no tiene permiso para esta página')

@login_required
def verDesempenioSucursal(request):
	if request.user.groups.filter(name="Supervisor").exists():
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
	else:
		raise Http404('Error, no tiene permiso para esta página')
@login_required
def verIngrRetiEstudiantesSuc(request):
	if request.user.groups.filter(name="Supervisor").exists():
		if request.method == 'POST':
			fechaInicio = datetime.strptime(request.POST.get('fecha_inicio'), '%Y-%m-%d')
			fechaFin = datetime.strptime(request.POST.get('fecha_fin'), '%Y-%m-%d')
			if fechaFin>fechaInicio:
				if request.POST.get('previa') == '':
					return verSalidaIngreSalEstudiantesSuc(request)
				else:
					fechaInicio = request.POST.get('fecha_inicio')
					fechaFin = request.POST.get('fecha_fin')
					return redirect('pdf_ing_ret_estu_su', fechaInicio, fechaFin)
			else:
				msj = "Fecha Fin debe ser mayor a Fecha Inicio"
				print msj
				esDanger = True
				fechaHoy = datetime.now().date()
				fechaInicio = fechaHoy - timedelta(days = 30)
				context = {
				'fechaHoy' : fechaHoy,
				'fechaInicio' : fechaInicio,
				'msj' : msj,
				}
				return render(request, 'supervisor/ingre-ret-estudiantes-suc.html', context)

		fechaHoy = datetime.now().date()
		fechaInicio = fechaHoy - timedelta(days = 30)
		context = {
			'fechaHoy' : fechaHoy,
			'fechaInicio' : fechaInicio,
			'msj' : ''
		}
		return render(request, 'supervisor/ingre-ret-estudiantes-suc.html', context)
	else:
		raise Http404('Error, no tiene permiso para esta página')



## Salidas
@login_required
def verSalidaIngresoEconSuc(request):
	if request.user.groups.filter(name="Supervisor").exists():
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
	else:
		raise Http404('Error, no tiene permiso para esta página')

@login_required
def verSalidaDesempenioSucursal(request):
	if request.user.groups.filter(name="Supervisor").exists():
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
	else:
		raise Http404('Error, no tiene permiso para esta página')
@login_required
def verSalidaIngreSalEstudiantesSuc(request):
	if request.user.groups.filter(name="Supervisor").exists():
		fechaHoy = datetime.now().date()
		fechaInicio = datetime.strptime(request.POST.get('fecha_inicio'), '%Y-%m-%d')
		fechaFin = datetime.strptime(request.POST.get('fecha_fin'), '%Y-%m-%d')
		sucursales = consultaInsRetEstuSuc(fechaInicio, fechaFin)
		for sucursal in sucursales:
			print sucursal[0]
		context = {
			'fechaHoy' : fechaHoy,
			'fechaInicio': fechaInicio,
			'fechaFin': fechaFin,
			'sucursales': sucursales,
		}
		return render(request, 'supervisor/sal-ingre-ret-estudiantes-suc.html', context)
	else:
		raise Http404('Error, no tiene permiso para esta página')

@login_required
def verSalidaDemandaCarrerasSuc(request):
	if request.user.groups.filter(name="Supervisor").exists():
		fechaHoy = datetime.now().date()
		sucursales = consultaDemandaCarreras()

		for sucursal in sucursales:
			print sucursal
		context = {
			'fechaHoy' : fechaHoy,
			'sucursales': sucursales,
		}
		return render(request, 'supervisor/sal-demanda-carreras.html', context)
	else:
		raise Http404('Error, no tiene permiso para esta página')

@login_required
def verSalidaEmpleadosSuc(request):
	if request.user.groups.filter(name="Supervisor").exists():
		fechaHoy = datetime.now().date()
		sucursales = consultaEmpleadosSuc()
		context = {
			'fechaHoy' : fechaHoy,
			'sucursales': sucursales,
		}
		return render(request, 'supervisor/sal-empleados-sucursal.html', context)
	else:
		raise Http404('Error, no tiene permiso para esta página')



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

class RepIngRetEstSucursal(PDFTemplateView):
	filename = 'Reporte_Ingresos_Retiros_Suc.pdf'
	template_name = 'supervisor/rep-ing-ret-est-suc.html'
	show_content_in_browser=True ###Para no descargar automaticamente
	###Para agregar context manuales
	def get_context_data(self, **kwargs):
		context = super(RepIngRetEstSucursal, self).get_context_data(**kwargs)
		fechaInicio = datetime.strptime(self.kwargs['fechaInicio'], '%Y-%m-%d')
		fechaFin = datetime.strptime(self.kwargs['fechaFin'], '%Y-%m-%d')
		context['fechaHoy'] = datetime.now().date()
		context['fechaInicio'] = fechaInicio
		context['fechaFin'] = fechaFin
		context['sucursales'] = consultaInsRetEstuSuc(fechaInicio, fechaFin)
		return context

class RepDemandaCarrerasSuc(PDFTemplateView):
	filename = 'Reporte_Demanda_Suc.pdf'
	template_name = 'supervisor/rep-demanda-carreras.html'
	show_content_in_browser=True ###Para no descargar automaticamente
	###Para agregar context manuales
	def get_context_data(self, **kwargs):
		context = super(RepDemandaCarrerasSuc, self).get_context_data(**kwargs)
		context['fechaHoy'] = datetime.now().date()
		context['sucursales'] = consultaDemandaCarreras()
		return context

class RepEmpleadosSuc(PDFTemplateView):
	filename = 'Reporte_Empleados_Suc.pdf'
	template_name = 'supervisor/rep-empleados-sucursal.html'
	show_content_in_browser=True ###Para no descargar automaticamente
	###Para agregar context manuales
	def get_context_data(self, **kwargs):
		context = super(RepEmpleadosSuc, self).get_context_data(**kwargs)
		context['fechaHoy'] = datetime.now().date()
		context['sucursales'] = consultaEmpleadosSuc()
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

def consultaInsRetEstuSuc(fechaInicio, fechaFin):
	with connections['default'].cursor() as cursorSG:
		cursorSG.execute("""
			select municipio_sucursal, telefono_sucursal, direccion_sucursal,
    		sum(case when estado_id = 2 then 1 else 0 end) as inscritos,
    		sum(case when estado_id = 8 then 1 else 0 end) as retirados
			from db_app_sucursal INNER JOIN  db_app_alumno ON codigo_sucursal=sucursal_id 
			INNER JOIN db_app_detalleestado ON codigo=alumno_id 
			where fecha_detalle_e between '{}' and '{}'
			group by municipio_sucursal, telefono_sucursal, direccion_sucursal
			order by inscritos desc
		""".format(datetime.strftime(fechaInicio,'%Y-%m-%d'), datetime.strftime(fechaFin, '%Y-%m-%d')))
		return cursorSG.fetchall()


def consultaDemandaCarreras():
	sucursales =Sucursal.objects.all()
	suc_list = []
	for suc in sucursales:
		with connections['default'].cursor() as cursorSG:
			cursorSG.execute("""
				select T1.municipio_sucursal, T1.telefono_sucursal, T1.direccion_sucursal, T1.nombre_carrera, maxi, T2.nombre_carrera, mini from
				(select municipio_sucursal, telefono_sucursal, direccion_sucursal, nombre_carrera, count(codigo_carrera) as maxi
				from db_app_sucursal INNER JOIN  db_app_carrera ON codigo_sucursal=sucursal_id 
				INNER JOIN db_app_expediente ON codigo_carrera=carrera_id INNER JOIN db_app_alumno
				ON alumno_id=codigo
				where codigo_sucursal='{}'
				group by municipio_sucursal, telefono_sucursal, direccion_sucursal,nombre_carrera
				order by maxi desc limit 1) T1
				inner JOIN
				(select municipio_sucursal,nombre_carrera, count(codigo_carrera) as mini
				from db_app_sucursal INNER JOIN  db_app_carrera ON codigo_sucursal=sucursal_id 
				INNER JOIN db_app_expediente ON codigo_carrera=carrera_id INNER JOIN db_app_alumno
				ON alumno_id=codigo
				where codigo_sucursal='{}'
				group by municipio_sucursal, telefono_sucursal, direccion_sucursal,nombre_carrera
				order by mini limit 1) T2 on T1.municipio_sucursal = T2.municipio_sucursal
				""".format(str(suc.codigo_sucursal),str(suc.codigo_sucursal)))
			for cur in cursorSG.fetchall():
				suc_list.append(cur)

	return suc_list

def consultaEmpleadosSuc():
	with connections['default'].cursor() as cursorSG:
		cursorSG.execute("""
			select T1.municipio_sucursal, T1.telefono_sucursal, T1.direccion_sucursal, T2.nombre, T1.cant from
			(select municipio_sucursal, telefono_sucursal, direccion_sucursal, codigo_sucursal, count(sucursal_id) as cant
			from db_app_sucursal INNER JOIN  db_app_empleado ON codigo_sucursal=sucursal_id 
			group by municipio_sucursal, telefono_sucursal, direccion_sucursal, codigo_sucursal
			order by cant desc)T1
			INNER JOIN
			(select sucursal_id, nombre from db_app_empleado where tipo='Dir')T2 on T1.codigo_sucursal=T2.sucursal_id
		""")
		return cursorSG.fetchall()
