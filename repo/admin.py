from django.contrib import admin

# Register your models here.
from reg.models import UserProfile
from .models import *

class BookAuthorAdmin(admin.ModelAdmin):
	list_display = ('author_last_name', 'author_first_name', 'author_middle_name')
	search_fields = ('author_last_name', 'author_first_name', 'author_middle_name')
	list_filter = ('author_last_name',)
	ordering = ('-author_last_name',)

class LibraryBookAdmin(admin.ModelAdmin):
	list_display = ('book_title', 'book_author_id', 'category','quantity', 'number_borrowed')
	search_fields = ('book_title',)
	fields = ('book_title', 'book_author_id', 'category')

class SingleBookAdmin(admin.ModelAdmin):
	list_display = ('book_id', 'serial_number')

	def save_model(self, request, obj, form, change):
		admin.ModelAdmin.save_model(self, request, obj, form, change)

		if not change:
			obj.book_id.quantity += 1
		if not obj.is_available_returned:
			obj.book_id.number_borrowed += 1
		if obj.is_available_returned and obj.book_id.number_borrowed > 0:
			obj.book_id.number_borrowed -= 1
		obj.book_id.save()




admin.site.register(UserProfile)
admin.site.register(LibraryBook, LibraryBookAdmin)
admin.site.register(SingleBook, SingleBookAdmin)
admin.site.register(BookAuthors, BookAuthorAdmin)
admin.site.register(BorrowingLog)
admin.site.register(BookCategory)