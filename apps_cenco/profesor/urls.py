from django.conf.urls import url
from apps_cenco.profesor import views

urlpatterns = [
    
#Entradas
	url(r'^desempenio_estudiantil/$', views.verDesempenioEstudiantil, name="desempenio_estudiantil"),
	url(r'^inasistencia_estudiantil/$', views.verInasistenciaEstudiantil, name="inasistencia_estudiantil"),


#PDFS
	url(r'^pdf_desempenio_estudiantil/(?P<grupo>\d{1})$',views.RepDesempenioEstudiantil.as_view(), name='pdf_desempenio_estudiantil'),

]