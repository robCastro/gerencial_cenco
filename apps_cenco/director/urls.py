from django.conf.urls import url
from apps_cenco.director import views
from wkhtmltopdf.views import PDFTemplateView

urlpatterns = [

	#Entradas
	url(r'^ingreso_retiros_estudiantes/$', views.verIngresosRetirosEstudiantes, name="ingreso_retiros_estudiantes"),
	url(r'^desempenio_didactico/$', views.verDesempenioDidactico, name="desempenio_didactico"),
	url(r'^ingreso_econ_suc/$', views.verIngresoEconSuc, name="ingreso_econ_suc"),
	url(r'^desempenio_sucursal/$', views.verDesempenioSucursal, name="desempenio_sucursal"),

    url(r'^moras_estudiantiles/$', views.verMorasEstudiantiles, name="moras_estudiantiles"),

	#Salidas
	url(r'^salida_ingreso_retiros_estudiantes/$',
		views.verSalidaIngresosRetirosEstudiantes,
		name="sal_ingreso_retiros_estudiantes"),

	url(r'^salida_desempenio_sucursal/$',
		views.verSalidaDesempenioSucursal,
		name="sal_desempenio_sucursal"),

	url(r'^salida_ingreso_econ_suc/$',
		views.verSalidaIngresoEconSuc,
		name="sal_ingreso_econ_suc"),

	url(r'^sal_demanda_carreras/$', views.verSalidaDemandaCarreras, name="demanda_carreras"),
	

	#PDFS
	url(r'^pdf_ingreso_retiros_estudiantes/(?P<idSucursal>\d{1})/(?P<fechaInicio>\d{4}-\d{2}-\d{2})/(?P<fechaFin>\d{4}-\d{2}-\d{2})/(?P<tipo>\d{1})$', views.RepIngresosRetirosEstudiantes.as_view(), name='pdf_ingreso_retiros_estudiantes'),
	#url(r'^pdf_ingreso_retiros_estudiantes/$', views.RepIngresosRetirosEstudiantes.as_view(), name='pdf_ingreso_retiros_estudiantes'),

	url(r'^pdf_demanda_carreras/$', views.RepDemandaCarreras.as_view(), name='pdf_demanda_carreras'),
	url(r'^pdf_moras_estudiantiles/(?P<grupo>\d{1,2})/(?P<cantidad>\d{1,2})$',views.RepMorasEstudiantiles.as_view(), name='pdf_moras_estudiantiles'),
]