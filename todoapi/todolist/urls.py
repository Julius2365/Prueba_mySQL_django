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
  path('crear/', views.crear_libro, name='crear-libro'),
  path('lista/', views.lista_libros, name='lista-libros'),
  path('actualizar/<int:pk>/', views.actualizar_libro, name='actualizar-libro'),
  path('eliminar/<int:pk>/', views.eliminar_libro, name='eliminar-libro'),
]