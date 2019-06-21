# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect

from datetime import datetime, timedelta
from wkhtmltopdf.views import PDFTemplateView
from django.contrib.auth.decorators import permission_required, login_required
from django.http import Http404, HttpResponse
from apps_cenco.db_app.models import Inscripcion, Estado, Empleado, Sucursal, Grupo, Carrera
from django.views.generic import ListView

##Entradas
@login_required
def verIngresosRetirosEstudiantes(request):
	if request.user.groups.filter(name="Director").exists():
		if request.method == 'POST':
			if (request.POST.get('previa') == ''):
				return verSalidaIngresosRetirosEstudiantes(request)
			else:
				fechaInicio = request.POST.get('fecha_inicio')
				fechaFin = request.POST.get('fecha_fin')
				sucursal = Empleado.objects.get(username = request.user).sucursal
				tipo = int(request.POST.get('tipo'))
				return redirect('pdf_ingreso_retiros_estudiantes', sucursal.codigo_sucursal, fechaInicio, fechaFin, tipo)
		fechaHoy = datetime.now().date() ###Fecha hoy se usa como fecha fin en front
		fechaInicio = fechaHoy - timedelta(days = 30)
		context = {
			'fechaHoy' : str(fechaHoy),
			'fechaInicio' : str(fechaInicio),
		}
		return render(request, 'director/ingresos-retiros-estudiantes.html', context)
	else:
		raise Http404('Error, no tiene permiso para esta página')

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

@login_required
def verMorasEstudiantiles(request):
	if request.user.groups.filter(name="Director").exists():
		sucursal = Empleado.objects.get(username=request.user).sucursal
		if request.method == 'POST':
			if 'vistaPrevia' in request.POST:
				return verSalidaMorasEstudiantiles(request)
			if 'descargar' in request.POST:
				fechaHoy = str((datetime.now().date().strftime("%d/%m/%Y")))
				grupo = int(request.POST.get('grupo'))
				cantidad = request.POST.get('cantidad')
				return redirect('pdf_desempenio_estudiantil', grupo)
		else:
			grupos = Grupo.objects.raw(
				"SELECT gr.codigo FROM db_app_grupo as gr join db_app_empleado as em on gr.profesor_id=em.codigo "
				"join db_app_sucursal as s on s.codigo_sucursal=em.sucursal_id "
				"where gr.activo_grupo=True and em.sucursal_id="+ str(sucursal.codigo_sucursal)+
				"order by gr.codigo"
			)
			context = {
				'grupos': grupos,
			}
			return render(request, 'director/moras-estudiantiles.html', context)
	else:
		raise Http404('Error, no tiene permiso para esta página')

##Salidas
def verSalidaIngresosRetirosEstudiantes(request):
	if request.method == 'POST':
		fechaHoy = datetime.now().date()
		detalles = None
		retiros = None
		tipo = int(request.POST.get('tipo'))
		sucursal = Empleado.objects.get(username = request.user).sucursal
		if tipo == 1 or tipo == 3:
			detalles = consultaIngresosRetirosEstudiantes(request.POST.get('fecha_inicio'), request.POST.get('fecha_fin'), 'Inscrito', sucursal)['detalles']
		if tipo == 2 or tipo == 3:
			retiros = consultaIngresosRetirosEstudiantes(request.POST.get('fecha_inicio'), request.POST.get('fecha_fin'), 'Retirados', sucursal)['detalles']
		context = {
			'fechaHoy' : fechaHoy,
			'fechaInicio' : datetime.strptime(request.POST.get('fecha_inicio'), "%Y-%m-%d"),
			'fechaFin' : datetime.strptime(request.POST.get('fecha_fin'), "%Y-%m-%d"),
			'tipo' : tipo,
			'sucursal' : sucursal,
			'detalles' : detalles,
			'retiros' : retiros
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

def verSalidaMorasEstudiantiles(request):
	sucursal = Empleado.objects.get(username=request.user).sucursal
	if request.method == 'POST':
		fechaHoy = str((datetime.now().date().strftime("%d/%m/%Y")))
		grupo = int(request.POST.get('grupo'))
		cantidad = request.POST.get('cantidad')
		if grupo == 0:
			grupos=Grupo.objects.raw(
				"SELECT gr.codigo FROM db_app_grupo as gr join db_app_empleado as em on gr.profesor_id=em.codigo "
				"join db_app_sucursal as s on s.codigo_sucursal=em.sucursal_id "
				"where gr.activo_grupo=True and em.sucursal_id=" + str(sucursal.codigo_sucursal) +
				"order by gr.codigo"
			)
		else:
			grupos = Grupo.objects.filter(codigo=grupo).order_by('codigo')
		context = {
			'grupo': grupo,
			'fechaHoy': fechaHoy,
			'grupos': grupos,
		}
		return render(request, 'director/sal-moras-estudiantiles.html', context)

@login_required
def verSalidaDemandaCarreras(request):
	if request.user.groups.filter(name="Director").exists():
		sucursal = Empleado.objects.get(username=request.user).sucursal
		fechaHoy = str((datetime.now().date().strftime("%d/%m/%Y")))
		carreras=Carrera.objects.raw(
			"SELECT ca.codigo_carrera, count(e.alumno_id) as cant_alumnos "
			"FROM db_app_carrera as ca join db_app_sucursal as s on ca.sucursal_id=s.codigo_sucursal "
			"join db_app_expediente as e on ca.codigo_carrera=e.carrera_id "
			"where ca.activo_carrera=True and e.activo_expediente=True and s.codigo_sucursal=" + str(sucursal.codigo_sucursal) +
			" group by ca.codigo_carrera "
			"order by cant_alumnos desc"
		)
		context = {
			'fechaHoy': fechaHoy,
			'carreras': carreras,
		}
		return render(request, 'director/sal-demanda-carreras.html', context)
	else:
		raise Http404('Error, no tiene permiso para esta página')



##Reportes
class RepIngresosRetirosEstudiantes(PDFTemplateView):
	filename = 'Reporte_Estudiantes.pdf'
	template_name = 'director/rep-ingresos-retiros-estudiantes.html'
	show_content_in_browser=True ###Para no descargar automaticamente
	###Para agregar context manuales
	def get_context_data(self, **kwargs):
		context = super(RepIngresosRetirosEstudiantes, self).get_context_data(**kwargs)
		tipo = int(self.kwargs['tipo'])
		idSucursal = int(self.kwargs['idSucursal'])
		sucursal = Sucursal.objects.get(codigo_sucursal = idSucursal)
		if tipo < 1 or tipo > 3:
			tipo = 3
		context['fechaHoy'] = datetime.now().date()
		fechaInicio = datetime.strptime(self.kwargs['fechaInicio'], '%Y-%m-%d')
		fechaFin = datetime.strptime(self.kwargs['fechaFin'], '%Y-%m-%d')
		context['fechaInicio'] = fechaInicio
		context['fechaFin'] = fechaFin
		context['detalles'] = None
		context['retiros'] = None
		if tipo == 1 or tipo == 3:
			context['detalles'] = consultaIngresosRetirosEstudiantes(fechaInicio, fechaFin, 'Inscrito', sucursal)['detalles']
		if tipo == 2 or tipo == 3:
			context['retiros'] = consultaIngresosRetirosEstudiantes(fechaInicio, fechaFin, 'Retirados', sucursal)['detalles']
		return context


class RepDemandaCarreras(PDFTemplateView):
	filename = 'demanda_carreras.pdf'
	template_name = 'director/rep-demanda-carreras.html'
	show_content_in_browser = True  ###Para no descargar automaticamente

	###Para agregar context manuales
	def get_context_data(self, **kwargs):
		context = super(RepDemandaCarreras, self).get_context_data(**kwargs)
		context['fechaHoy'] = str((datetime.now().date().strftime("%d/%m/%Y")))
		sucursal = Empleado.objects.get(username=self.request.user).sucursal
		carreras = Carrera.objects.raw(
			"SELECT ca.codigo_carrera, count(e.alumno_id) as cant_alumnos "
			"FROM db_app_carrera as ca join db_app_sucursal as s on ca.sucursal_id=s.codigo_sucursal "
			"join db_app_expediente as e on ca.codigo_carrera=e.carrera_id "
			"where ca.activo_carrera=True and e.activo_expediente=True and s.codigo_sucursal=" + str(
				sucursal.codigo_sucursal) +
			" group by ca.codigo_carrera "
			"order by cant_alumnos desc"
		)
		context['carreras'] = carreras
		return context


##Consultas Auxiliares
def consultaIngresosRetirosEstudiantes(fechaInicio, fechaFin, tipo_estado, sucursal):
	estado = Estado.objects.get(tipo_estado = tipo_estado)
	for carrera in sucursal.carrera_set.all():
		print carrera.nombre_carrera
	detalles = estado.detalleestado_set.filter(fecha_detalle_e__range=(fechaInicio, fechaFin), alumno__sucursal = sucursal)
	context = {
		'detalles' : detalles
	}
	return context

