from django.conf.urls import url
from apps_cenco.director import views

urlpatterns = [
	url(r'^ingreso_retiros_estudiantes/$', views.verIngresosRetirosEstudiantes, name="ingreso_retiros_estudiantes"),
]