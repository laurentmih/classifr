from django.urls import path

from . import views

app_name = 'classify'

urlpatterns = [
	path('', views.index, name='index'),
	path('classify/', views.classify, name='classify'),
	path('export/', views.export, name='export'),
	path('demo/', views.demo, name='demo'),
]