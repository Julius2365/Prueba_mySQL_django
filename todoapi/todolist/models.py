from django.db import models

from django.db import models

class Libro(models.Model):
    titulo = models.CharField(max_length=100)
    autor = models.CharField(max_length=100)

class Todo(models.Model):
  algun_criterio = models.BooleanField(default=True)
# Create your models here.
class Todo(models.Model):
  id = models.AutoField(
    primary_key=True
  )

  text = models.TextField(
    max_length=1000,
    null=False,
    blank=False
  )

  creation_date = models.DateTimeField(
    auto_now_add=True,
    null=False,
    blank=False
  )

  last_updated = models.DateTimeField(
    auto_now=True,
    null=False,
    blank=False
  )

  class Meta:
    db_table = 'Todos'
