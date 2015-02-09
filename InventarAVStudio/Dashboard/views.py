from django.shortcuts import render_to_response, redirect
from Inventar.models import Geraet, GeraeteTyp
from django.db.models import Q
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from Dashboard.models import DashboardCategory, DashboardEntry

@login_required
def index(request):
	categories = DashboardCategory.objects.all().order_by('name')
	catlist = []

	for c in categories:
		catlist.append(list(c.dashboardentry_set.all()))
		
	
	return render_to_response("dashboard/index.html", {'categories': categories, 'entries': catlist,'active': 'dashboard'}, context_instance=RequestContext(request))
	
