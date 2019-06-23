from django.conf.urls import url
from apps_cenco.supervisor import views
from wkhtmltopdf.views import PDFTemplateView

urlpatterns = [

	#Entradas
	url(r'^ingreso_econ_suc/$', views.verIngresoEconSuc, name="ingreso_econ_suc"),
	url(r'^desempenio_sucursal/$', views.verDesempenioSucursal, name="desempenio_sucursal"),
	url(r'^ingreso_retiros_estudiantes_suc/$', views.verIngrRetiEstudiantesSuc, name="ingreso_retiros_estudiantes_suc"),

	#Salidas
	url(r'^salida_ingreso_econ_suc/$',
		views.verSalidaIngresoEconSuc,
		name="sal_ingreso_econ_suc"),
	url(r'^salida_desempenio_sucursal/$',
		views.verSalidaDesempenioSucursal,
		name="sal_desempenio_sucursal"),
	url(r'^salida_demanda_carreras/$',
		views.verSalidaDemandaCarrerasSuc,
		name="salida_demanda_carreras"),
	url(r'^salida_empleados_sucursal/$',
		views.verSalidaEmpleadosSuc,
		name="salida_empleados_sucursal"),

	#PDFS
	url(r'^pdf_ingreso_econ_suc/(?P<fechaInicio>\d{4}-\d{2}-\d{2})/(?P<fechaFin>\d{4}-\d{2}-\d{2})$', 
		views.RepIngresosEconSucursal.as_view(),
		name='pdf_ingreso_econ_suc'),
	url(r'^pdf_desempenio_sucursal/(?P<fechaInicio>\d{4}-\d{2}-\d{2})/(?P<fechaFin>\d{4}-\d{2}-\d{2})$',
		views.RepDesempenioSucursal.as_view(),
		name='pdf_ingreso_econ_suc'),
	url(r'^pdf_ing_ret_estu_su/(?P<fechaInicio>\d{4}-\d{2}-\d{2})/(?P<fechaFin>\d{4}-\d{2}-\d{2})$',
		views.RepIngRetEstSucursal.as_view(),
		name='pdf_ing_ret_estu_su'),
	url(r'^pdf_demanda_carreras/$',
		views.RepDemandaCarrerasSuc.as_view(),
		name='pdf_demanda_carreras'),
	url(r'^pdf_empleados_suc/$',
		views.RepEmpleadosSuc.as_view(),
		name='pdf_empleados_suc'),
]