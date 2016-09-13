from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import *
from django.contrib.auth.decorators import login_required
from repo.forms import UserForm
from django.core.urlresolvers import reverse
from django.utils import timezone

def index(request):
	return HttpResponse("Welcome to Library")

#@login_required(login_url='/login')
def home(request):
	return render(request, 'repo/home.html')

def login(request):
	return redirect('/reg/login')
	# return HttpResponse("Welcome to the login page")

def register(request):
	return HttpResponse("Welcome to register")

@login_required(login_url='reg:login')
def library(request):
	single_books = SingleBook.objects.all()
	#books = LibraryBook.objects.all()
	return render(request, 'repo/library.html', {'single_books': single_books})
	# return HttpResponse("Welcome to library")

def results(request):
	return render(request, 'repo/results.html')

@login_required(login_url='reg:login')
def borrow(request, sn):
	user_id = request.user.id
	sn = str(sn)
	try:
		get_singles = SingleBook.objects.get(serial_number=sn) 
		#get_book = LibraryBook.objects.get(pk=pk)
		get_user = User.objects.get(pk=user_id)
		#get_availability = AvailabilityStatus.objects.get(availability_name='borrowed')
	except User.DoesNotExist or SingleBook.DoesNotExist:
		raise Http404("Book not found")
	if (get_singles.is_available_returned) and get_singles.book_id.number_borrowed < get_singles.book_id.quantity:
		timer = timezone.now() + timezone.timedelta(days=1)
		single_quantity = int(get_singles.book_id.number_borrowed) + 1
		get_singles.book_id.number_borrowed = single_quantity
		get_singles.is_available_returned = False
		#get_book.availability_status_id = get_availability.id
		create_log = BorrowingLog.objects.create(
			comment='Book borrowed',
			lend_date=timezone.now(), 
			expected_return_date=timer, 
			bookid_id=get_singles.book_id.id, 
			userid_id=user_id, 
			log_name_id=get_singles.serial_number
			)
		create_log.save()
		get_singles.save()
		#get_book.save()

		return HttpResponseRedirect(reverse('repo:library'))

	return redirect('/repo/library')