from django.conf.urls import url
from apps_cenco.profesor import views

urlpatterns = [
    
#Entradas
	url(r'^desempenio_estudiantil/$', views.verDesempenioEstudiantil, name="desempenio_estudiantil"),
	url(r'^inasistencia_estudiantil/$', views.verInasistenciaEstudiantil, name="inasistencia_estudiantil"),


#PDFS
	url(r'^pdf_desempenio_estudiantil/(?P<grupo>\d{1,2})$',views.RepDesempenioEstudiantil.as_view(), name='pdf_desempenio_estudiantil'),
	url(r'^pdf_inasistencia_estudiantil/(?P<grupo>\d{1,2})/(?P<fechaInicio>\d{4}-\d{2}-\d{2})/(?P<fechaFin>\d{4}-\d{2}-\d{2})/(?P<cantidad>\d{1,2})$', views.RepInasistenciaEstudiantil.as_view(), name='pdf_inasistencia_estudiantil'),

]