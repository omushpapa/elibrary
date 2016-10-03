from django.shortcuts import render
from .models import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .forms import CardForm, TodoListForm, MoveCardForm
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse, reverse_lazy
from hashids import Hashids
# from django.contrib.auth.forms import UserCreationForm

hashids = Hashids(salt='2016-08-18 16:27:22 IiTNmll0 ATn1ViSu', alphabet='123456789abdefghijmdncklopqrstuvwxy0', min_length=7)

# Any user can edit/update any list, card, item 
# Any user can create a card/item in another user's

def todolists(request):
	user_id = request.user.id
	todo_lists = TodoList.objects.filter(user=user_id).order_by('id')
	return render(request, 'todo/todos.html', {'todo_lists': todo_lists})

class UpdateTodoList(UpdateView):
	model = TodoList
	fields = ('todo_name', 'publicity_status',)
	template_name = 'todo/todolist_new.html'
	success_url = reverse_lazy('todo:todo_lists')

	def get_object(self, queryset=None):
		try:
			pk = hashids.decode(self.kwargs['list_id'])[0]
		except IndexError:
			raise Http404
		try:
			obj = TodoList.objects.get(id=pk, user=self.request.user)
		except TodoList.DoesNotExist:
			raise Http404		
		return obj

def cards(request, card_id):
	try:
		card_id = hashids.decode(card_id)[0]
	except IndexError:
		raise Http404
	card_form = CardForm()
	cards = Card.objects.filter(id=card_id)
	card_list = TodoList.objects.filter(card__in=cards)
	items = cards[0].todo_item.all()

	return render(request, 'todo/cards.html', {
		'cards': cards, 
		'card_list': card_list,
		'items': items,
		'card_form': CardForm()
		})

class CreateList(CreateView):
	model = TodoList
	fields = ('todo_name', 'publicity_status',)
	template_name = 'todo/new_instance.html'
	success_url = reverse_lazy('todo:todo_lists')

	def form_valid(self, form):
		obj = form.save(commit=False)
		obj.user = self.request.user
		return super(CreateList, self).form_valid(form)

class CreateCard(CreateView):
	model = Card
	fields = ('card_name', 'description',)
	template_name = 'todo/new_instance.html'
	success_url = reverse_lazy('todo:todo_lists')

	def form_valid(self, form):
		try:
			list_id = hashids.decode(self.kwargs['list_id'])[0]
		except IndexError:
			raise Http404
		obj = form.save(commit=False)
		todo_list = TodoList.objects.filter(pk=list_id)
		obj.save()
		todo_list[0].card.add(obj)
		return super(CreateCard, self).form_valid(form)

class UpdateCard(UpdateView):
	model = Card
	fields = ('card_name', 'description',)
	template_name = 'todo/card_new.html'
	success_url = reverse_lazy('todo:todo_lists')

	def get_object(self, queryset=None):
		try:
			card_id = hashids.decode(self.kwargs['card_id'])[0]
		except IndexError:
			raise Http404
		obj = Card.objects.get(id=card_id)
		return obj

class CreateTodoItem(CreateView):
	model = TodoItem
	fields = ('item_name', 'item_description', 'status', 'is_done',)
	template_name = 'todo/new_instance.html'
	success_url = reverse_lazy('todo:todo_lists')

	def form_valid(self, form):
		obj = form.save(commit=False)
		try:
			card_id = hashids.decode(self.kwargs['card_id'])[0]
		except IndexError:
			raise Http404
		try:
			card = Card.objects.filter(pk=card_id)
		except UnboundLocalError:
			raise Http404
		obj.save()
		card[0].todo_item.add(obj)
		return super(CreateTodoItem, self).form_valid(form)

class UpdateTodoItem(UpdateView):
	model = TodoItem
	fields = ('item_name', 'item_description', 'status', 'is_done',)
	template_name = 'todo/todoitem_new.html'
	success_url = reverse_lazy('todo:todo_lists')

	def get_object(self, queryset=None):
		try:
			item_id = hashids.decode(self.kwargs['item_id'])[0]
		except IndexError:
			raise Http404
		try:
			obj = TodoItem.objects.get(id=item_id)
		except UnboundLocalError:
			raise Http404
		return obj

def move_card(request, card_id):
	try:
		card_id = hashids.decode(card_id)[0]
	except IndexError:
		raise Http404
	card = Card.objects.filter(id=card_id)[0]

	if request.method == 'POST':
		form = MoveCardForm(request.user, request.POST)

		if form.is_valid():
			new_card_id = request.POST.get('card_id')
			
			new_card = Card.objects.filter(id=int(new_card_id))
			todo = TodoList.objects.filter(id=form.cleaned_data['todo_name'].id)[0]
			initial_todo = TodoList.objects.filter(card__in=new_card)
			initial_todo[0].card.remove(new_card[0])
			todo.card.add(new_card[0])

			return HttpResponseRedirect(reverse('todo:todo_lists'))
		else:
			HttpResponse('Error!')

	return render(request, 'todo/move_card.html', {'form': MoveCardForm(request.user), 'card': card})