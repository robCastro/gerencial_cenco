from django.conf.urls import url
from apps_cenco.director import views
from wkhtmltopdf.views import PDFTemplateView

urlpatterns = [

	#Entradas
	url(r'^ingreso_retiros_estudiantes/$', views.verIngresosRetirosEstudiantes, name="ingreso_retiros_estudiantes"),
	url(r'^desempenio_didactico/$', views.verDesempenioDidactico, name="desempenio_didactico"),
	


	#Salidas
	url(r'^salida_ingreso_retiros_estudiantes/$',
		views.verSalidaIngresosRetirosEstudiantes,
		name="sal_ingreso_retiros_estudiantes"),
	
	

	#PDFS
	url(r'^pdf_ingreso_retiros_estudiantes/(?P<idSucursal>\d{1})/(?P<fechaInicio>\d{4}-\d{2}-\d{2})/(?P<fechaFin>\d{4}-\d{2}-\d{2})/(?P<tipo>\d{1})$', 
		views.RepIngresosRetirosEstudiantes.as_view(), 
		name='pdf_ingreso_retiros_estudiantes'),
	url(r'^pdf_desempenio_didactico/(?P<idSucursal>\d{1})$', 
		views.RepDesempenioProfesores.as_view(), 
		name='pdf_desempenio_didactico'),

	
]	