from django.urls import path

from . import views

urlpatterns = [
  path('todos/', views.TodoListView.as_view()),
  path('todos/<int:id>/', views.TodoListView.as_view()),
  path('mi-endpoint/',views.mi_vista,name='mi-endpoint'),
  path('obtener-datos/', views.obtener_datos, name='obtener-datos'),
  path('endpoint-autenticado/', views.endpoint_autenticado, name='endpoint-autenticado'),
  path('endpoint-xml/', views.endpoint_xml, name='endpoint-xml'),
  path('endpoint-con-parametros/<str:parametro>/', views.endpoint_con_parametros, name='endpoint-con-parametros'),
]