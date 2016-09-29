from django.contrib import admin
from todo.models import *
from django.contrib import admin

class CardAdmin(admin.ModelAdmin):
	fieldsets = [
		('Card Data', {'fields': ['card_name', 'description']}),
		('Todo Items', {'fields': ['todo_item']}),
	]


admin.site.register(TodoList)
admin.site.register(Card, CardAdmin)
admin.site.register(TodoItem)