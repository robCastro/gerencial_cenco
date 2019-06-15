from django.conf.urls import url
from apps_cenco.director import views

urlpatterns = [
	url(r'^ingreso_retiros_estudiantes/$', views.verIngresosRetirosEstudiantes, name="ingreso_retiros_estudiantes"),
	url(r'^desempenio_didactico/$', views.verDesempenioDidactico, name="desempenio_didactico"),
	url(r'^ingreso_econ_suc/$', views.verIngresoEconSuc, name="ingreso_econ_suc"),
	url(r'^desempenio_sucursal/$', views.verDesempenioSucursal, name="desempenio_sucursal"),




	url(r'^salida_ingreso_retiros_estudiantes/$',
		views.verSalidaIngresosRetirosEstudiantes,
		name="sal_ingreso_retiros_estudiantes"),

	url(r'^salida_desempenio_sucursal/$',
		views.verSalidaDesempenioSucursal,
		name="sal_desempenio_sucursal"),

	url(r'^salida_ingreso_econ_suc/$',
		views.verSalidaIngresoEconSuc,
		name="sal_ingreso_econ_suc"),
	
]