from django.shortcuts import render_to_response, redirect
from Inventar.models import Geraet, GeraeteTyp
from django.db.models import Q
from django.template import RequestContext

def index(request):
	return redirect("/public/inventar/")

def public_inventar(request):
	geraete = Geraet.objects.filter(~Q(nummer=""))
	return render_to_response('public/inventar.html', {'geraete': geraete, 'no_navbar': True}, context_instance=RequestContext(request))

