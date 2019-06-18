from django.conf.urls import url
from apps_cenco.login import views

urlpatterns = [
	url(r'^etl/$', views.verPantallaETL, name="etl"),
]