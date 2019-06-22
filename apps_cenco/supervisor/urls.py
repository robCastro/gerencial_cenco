from django.conf.urls import url
from apps_cenco.supervisor import views
from wkhtmltopdf.views import PDFTemplateView

urlpatterns = [

	#Entradas
	url(r'^ingreso_econ_suc/$', views.verIngresoEconSuc, name="ingreso_econ_suc"),
	url(r'^ingreso_retiros_estudiantes_suc/$', views.verIngrRetiEstudiantesSuc, name="ingreso_retiros_estudiantes_suc"),

	#Salidas
	url(r'^salida_ingreso_econ_suc/$',
		views.verSalidaIngresoEconSuc,
		name="sal_ingreso_econ_suc"),

	#PDFS
	url(r'^pdf_ingreso_econ_suc/(?P<fechaInicio>\d{4}-\d{2}-\d{2})/(?P<fechaFin>\d{4}-\d{2}-\d{2})$', 
		views.RepIngresosEconSucursal.as_view(),
		name='pdf_ingreso_econ_suc'),
	url(r'^pdf_ing_ret_estu_su/(?P<fechaInicio>\d{4}-\d{2}-\d{2})/(?P<fechaFin>\d{4}-\d{2}-\d{2})$',
		views.RepIngRetEstSucursal.as_view(),
		name='pdf_ing_ret_estu_su'),
]