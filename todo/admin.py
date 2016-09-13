from django.contrib import admin
from todo.models import *

admin.site.register(TodoList)
admin.site.register(Card)
admin.site.register(TodoItem)