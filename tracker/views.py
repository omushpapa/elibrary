from django.shortcuts import render, render_to_response, get_list_or_404
from tracker.models import *
from django.views.generic import ListView, CreateView
from tracker.forms import *
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.models import User
from .models import Issue
from django.db.models import Q
import re
from django.template import RequestContext
from hashids import Hashids
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.utils.decorators import method_decorator
from repo.models import LibraryBook

@method_decorator(login_required, name='dispatch')
class NotificationListView(ListView):
    model = Notification
    template_name = "tracker/notifications.html"

@login_required(login_url='reg:login')
@permission_required('maintenance.add_maintenance', login_url='reg:login')
def maintenance(request):
    user_form = MaintenanceForm()
    user_id = request.user.id
    is_staffmember = request.user.groups.filter(name='StaffMember').exists()
    maintenance = Maintenance.objects.all().filter(requested_user=user_id)

    if request.method == 'POST':
        user_form = MaintenanceForm(request.POST)
        if user_form.is_valid():
            maintain = user_form.save(commit=False)
            maintain.requested_user = request.user
            maintain.save()
            
            return HttpResponseRedirect(reverse('tracker:maintenance'))
        else:
            return render(request, 'tracker/maintenance.html', {
                'maintenance_form': MaintenanceForm(),
                'maintenances': maintenance,
                'error_messages': 'No data entered!',
                })

    return render(request, 'tracker/maintenance.html', {
        'maintenance_form': MaintenanceForm(),
        'maintenances': maintenance,
        })

@login_required
def issue_view(request):
    user_form = IssueForm()
    user_id = request.user.id
    if Issue.objects.filter(user=user_id).count() > 0:
        issues = Issue.objects.filter(user=user_id)
    else:
        issues = None

    if request.method == 'POST':
        user_form = IssueForm(request.POST)
        if user_form.is_valid():
            issue = user_form.save(commit=False)
            issue.user = request.user
            issue.save()
            #return HttpResponse("Done")
            return HttpResponseRedirect(reverse('tracker:issues'))
        else:
            return HttpResponse(user_form)

    return render(request, 'tracker/issues.html', {
        'issue_form': IssueForm(),
        'issues': issues
        })

@method_decorator(login_required, name='dispatch')
class CreateDocument(CreateView):
    model = Document
    fields = ('title', 'url', 'document_category',)
    template_name = 'tracker/new_doc.html'

@method_decorator(login_required, name='dispatch')
class ListDocument(ListView):

    model = Document

@method_decorator(login_required, name='dispatch')
class ListMyDocument(ListView):

    model = Document
    template_name = 'tracker/document_list.html'

    def get_queryset(self):
        queryset = Document.objects.filter(user=self.request.user)
        return queryset

@method_decorator(login_required, name='dispatch')
class CreateDocument(CreateView):
    model = Document
    template_name = 'tracker/new_instance.html'
    fields = ('title', 'url', 'document_category',)
    success_url = reverse_lazy('tracker:my_documents')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return super(CreateDocument, self).form_valid(form)

@method_decorator(login_required, name='dispatch')
class ListDepartmentDocument(ListView):
    model = Document
    template_name = 'tracker/document_list.html'

    def get_queryset(self):
        dept = self.kwargs['dept_name']
        queryset = Document.objects.all().filter(document_category__category_name__contains=dept)
        return queryset

# snippet borrowed
def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:
        
        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
    
    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)] 

def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.
    
    '''
    query = None # Query to search for every search term        
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query

def search(request):
    query_string = ''
    found_entries = None
    if ('q' in request.GET) and request.GET['q'].strip():

        if ('type' in request.GET) and request.GET['type'].strip() and request.GET['type'] == 'books':
            query_string = request.GET['q']
        
            entry_query = get_query(query_string, ['book_title', 'category__category_name', 'book_author_id__author_first_name', 'book_author_id__author_last_name', ])
            
            found_entries = LibraryBook.objects.filter(entry_query).order_by('-id')

        else:
            query_string = request.GET['q']
            
            entry_query = get_query(query_string, ['title', 'document_category__category_name',])
            
            found_entries = Document.objects.filter(entry_query).order_by('-id')

    return render(request, 'tracker/search_results.html',
                          { 'query_string': query_string, 'found_entries': found_entries })

def try_hashids(request):
    query_string = ''
    query_dict = ''
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        hashids = Hashids(salt='2016-08-18 16:27:22 IiTNmll0 ATn1ViSu', alphabet='123456789AaBbHhDdNnCcKklLNo0', min_length=7)
        query_string = hashids.encode(int(query_string)) 
        query_decoded = hashids.decode(query_string)         
        #query_string = 'check'
        query_dict = {'query_string': query_string, 'decoded': query_decoded[0]}

    return render(request, 'tracker/try_hashids.html',
                          { 'query_dict': query_dict})