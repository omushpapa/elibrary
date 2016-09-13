from django.conf.urls import url
from tracker.views import *
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

app_name = 'tracker'
urlpatterns = [
	#url(r'^$', lambda r: HttpResponseRedirect('issues')),
	url(r'^issues/$', issue_view, name='issues'),
	url(r'^notifications/$', login_required(NotificationListView.as_view()), name='notifications'),
	url(r'^maintenance/$', maintenance, name='maintenance'),
	url(r'^documents/$', ListDocument.as_view(), name='documents'),
	url(r'^documents/department/(?P<dept_name>[A-Z a-z]+)/$', ListDepartmentDocument.as_view(), name='department_documents'),
	url(r'^documents/myuploads/$', ListMyDocument.as_view(), name='my_documents'),
	url(r'^documents/upload/$', CreateDocument.as_view(), name='upload_document'),
	url(r'^search/$', search, name='search_document'),
	url(r'^hashids/$', try_hashids, name='try_hashids'),
]