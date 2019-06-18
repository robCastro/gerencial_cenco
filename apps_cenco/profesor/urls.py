from django.conf.urls import url
from apps_cenco.profesor import views

urlpatterns = [
    
#Entradas
	url(r'^desempenio_estudiantil/$', views.verDesempenioEstudiantil, name="desempenio_estudiantil"),


#Salidas
	url(r'^salida_desempenio_estudiantil/$', views.verSalDesempenioEstudiantil, name="sal_desempenio_estudiantil"),


#PDFS
	url(r'^pdf_desempenio_estudiantil/$', views.RepDesempenioEstudiantil.as_view(), name='pdf_desempenio_estudiantil'),

]