from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from django.http import JsonResponse
from django.template import loader
from django.http import HttpResponse


from django.contrib.auth.decorators import  login_required
from .models import Todo
from .serializers import TodoSerializer

from django.shortcuts import render, get_object_or_404, redirect
from .models import Libro
from .forms import LibroForm

def crear_libro(request):
    if request.method == 'POST':
        form = LibroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista-libros')  # Redirige a la lista de libros después de crear uno
    else:
        form = LibroForm()
    return render(request, 'crear_libro.html', {'form': form})

def lista_libros(request):
    libros = Libro.objects.all()
    return render(request, 'lista_libros.html', {'libros': libros})

def actualizar_libro(request, pk):
    libro = get_object_or_404(Libro, pk=pk)
    if request.method == 'POST':
        form = LibroForm(request.POST, instance=libro)
        if form.is_valid():
            form.save()
            return redirect('lista-libros')
    else:
        form = LibroForm(instance=libro)
    return render(request, 'actualizar_libro.html', {'form': form})

def eliminar_libro(request, pk):
    libro = get_object_or_404(Libro, pk=pk)
    libro.delete()
    return redirect('lista-libros')




def endpoint_con_parametros(request, parametro):
  if request.method == 'GET':
    # Acceder a los parámetros de la solicitud GET
    valor = request.GET.get('clave', 'default')
    data = {'parametro': parametro, 'valor': valor}
    return JsonResponse(data)
  elif request.method == 'POST':
    # Acceder a los datos del cuerpo de la solicitud POST
    datos_post = request.POST.get('clave', 'default')
    data = {'parametro': parametro, 'datos_post': datos_post}
    return JsonResponse(data)



def endpoint_xml(request):
  datos = {'clave': 'valor'}  # Tus datos para convertir a XML
  template = loader.get_template('archivo_xml.xml')
  xml_data = template.render({'datos': datos})
  return HttpResponse(xml_data, content_type='application/xml')

def endpoint_autenticado(request):
  usuario= request.user
  data= {'mensaje':f'Hola,{usuario.username}!Este es un endpoint protegido'}
  return JsonResponse(data)

def obtener_datos(request):
  datos=Todo.objects.filter(id=True)
  data={'datos':list(datos.values())}
  return JsonResponse(data)


def mi_vista(request):
  data = {'mensaje': 'Hola, este es mi endpoint!'}
  return JsonResponse(data)
class TodoListView(
  APIView, # Basic View class provided by the Django Rest Framework
  UpdateModelMixin, # Mixin that allows the basic APIView to handle PUT HTTP requests
  DestroyModelMixin, # Mixin that allows the basic APIView to handle DELETE HTTP requests
):

  def get(self, request, id=None):
    if id:
      # If an id is provided in the GET request, retrieve the Todo item by that id
      try:
        # Check if the todo item the user wants to update exists
        queryset = Todo.objects.get(id=id)
      except Todo.DoesNotExist:
        # If the todo item does not exist, return an error response
        return Response({'errors': 'This todo item does not exist.'}, status=400)

      # Serialize todo item from Django queryset object to JSON formatted data
      read_serializer = TodoSerializer(queryset)

    else:
      # Get all todo items from the database using Django's model ORM
      queryset = Todo.objects.all()

      # Serialize list of todos item from Django queryset object to JSON formatted data
      read_serializer = TodoSerializer(queryset, many=True)

    # Return a HTTP response object with the list of todo items as JSON
    return Response(read_serializer.data)


  def post(self, request):
    # Pass JSON data from user POST request to serializer for validation
    create_serializer = TodoSerializer(data=request.data)

    # Check if user POST data passes validation checks from serializer
    if create_serializer.is_valid():

      # If user data is valid, create a new todo item record in the database
      todo_item_object = create_serializer.save()

      # Serialize the new todo item from a Python object to JSON format
      read_serializer = TodoSerializer(todo_item_object)

      # Return a HTTP response with the newly created todo item data
      return Response(read_serializer.data, status=201)

    # If the users POST data is not valid, return a 400 response with an error message
    return Response(create_serializer.errors, status=400)


  def put(self, request, id=None):
    try:
      # Check if the todo item the user wants to update exists
      todo_item = Todo.objects.get(id=id)
    except Todo.DoesNotExist:
      # If the todo item does not exist, return an error response
      return Response({'errors': 'This todo item does not exist.'}, status=400)

    # If the todo item does exists, use the serializer to validate the updated data
    update_serializer = TodoSerializer(todo_item, data=request.data)

    # If the data to update the todo item is valid, proceed to saving data to the database
    if update_serializer.is_valid():

      # Data was valid, update the todo item in the database
      todo_item_object = update_serializer.save()

      # Serialize the todo item from Python object to JSON format
      read_serializer = TodoSerializer(todo_item_object)

      # Return a HTTP response with the newly updated todo item
      return Response(read_serializer.data, status=200)

    # If the update data is not valid, return an error response
    return Response(update_serializer.errors, status=400)


  def delete(self, request, id=None):
    try:
      # Check if the todo item the user wants to update exists
      todo_item = Todo.objects.get(id=id)
    except Todo.DoesNotExist:
      # If the todo item does not exist, return an error response
      return Response({'errors': 'This todo item does not exist.'}, status=400)

    # Delete the chosen todo item from the database
    todo_item.delete()

    # Return a HTTP response notifying that the todo item was successfully deleted
    return Response(status=204)