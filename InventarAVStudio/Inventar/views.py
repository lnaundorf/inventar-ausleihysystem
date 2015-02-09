#coding: utf8
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.auth import logout
from Inventar.models import Geraet, GeraeteTyp
from Benutzer.models import Benutzer
from django.db.models import Q
from django.http import HttpResponse
from Inventar.forms import CreateGeraeteTypForm, GeraetForm
from django.contrib import messages

def login_or_index(request):
	if request.user.is_authenticated():
		return redirect('/inventar/')
	else:
		return redirect('/login/')

def logout_view(request):
	logout(request)
	return redirect('/login/')

@login_required
def index(request):
	geraete = Geraet.objects.all()
	schein_geraete = Geraet.objects.filter(status=Geraet.PENDING)
	return render_to_response('inventar/index.html', {'geraete': geraete, 'schein_geraete': schein_geraete}, context_instance=RequestContext(request))

@login_required
def info(request, id):
	schein_geraete = Geraet.objects.filter(status=Geraet.PENDING)

	try:
		g = Geraet.objects.get(pk=id)
	except Geraet.DoesNotExist:
		return render_to_response('inventar/info_404.html', {'id': id, 'schein_geraete': schein_geraete }, context_instance=RequestContext(request))

	schein_geraete = Geraet.objects.filter(status=Geraet.PENDING)
	return render_to_response('inventar/info.html', {'g': g, 'schein_geraete': schein_geraete }, context_instance=RequestContext(request))

@login_required
def filter_view(request):
	if 's' in request.GET:
		text = request.GET['s']
	else:
		text = ''

	geraete = Geraet.objects.filter(Q(nummer__icontains=text) | Q(typ__name__icontains=text) | Q(name__icontains=text) | Q(kommentar__icontains=text) | Q(ort__icontains=text));
	return render_to_response('inventar/table.html', {'geraete': geraete}, context_instance=RequestContext(request))


@login_required
def add(request):
	if request.method == 'GET':
		geraet_id = request.GET['id']
		try:
			g = Geraet.objects.get(pk=geraet_id)
		except Geraet.DoesNotExist:
			return 'error'
		
		g.status = Geraet.PENDING
		g.save()
		simple_list = []
		simple_list.append(g)
		return render_to_response('inventar/add.html', {'schein_geraete': simple_list}, context_instance=RequestContext(request))
	else:
		return HttpResponse('no GET')

@login_required
def remove(request):
	if request.method == 'GET':
		geraet_id = request.GET['id']
		try:
			g = Geraet.objects.get(pk=geraet_id)
		except Geraet.DoesNotExist:
			return HttpResponse('error')
		
		g.status = Geraet.AVAILABLE
		g.save()
		return HttpResponse('ok')
	else:
		return HttpResponse('no GET')

@login_required
def create(request):
	schein_geraete = Geraet.objects.filter(status=Geraet.PENDING)

	if request.method == "POST":
		form = GeraetForm(request.POST)
		if form.is_valid():
			g = form.save()
			return redirect('/inventar/')
	else:
		form = GeraetForm()

	return render_to_response('inventar/form.html', {'schein_geraete': schein_geraete, 'form': form, 'back': '/inventar/', 'submit': 'Erstellen', 'title': 'Neues Gerät erstellen'}, context_instance=RequestContext(request))

@login_required
def addType(request):
	if "name" in request.GET:
		name = request.GET['name']
		typ = GeraeteTyp(name=name)
		typ.save()

		return HttpResponse(typ.id)
	else:
		return HttpResponse("ERROR")

@login_required
def edit(request, id):
	schein_geraete = Geraet.objects.filter(status=Geraet.PENDING)

	try:
		g = Geraet.objects.get(pk=id)
	except Geraet.DoesNotExist:
		render_to_response('inventar/info_404.html', {'schein_geraete': schein_geraete}, context_instance=RequestContext(request))

	if request.method == "POST":
		form = GeraetForm(request.POST, instance=g)
		if form.is_valid():
			g = form.save()
			messages.add_message(request, messages.SUCCESS, 'Das Geraet ' + g.name + ' wurde erfolgreich bearbeitet.')
			return redirect('/inventar/info/' + id)
	else:
		form = GeraetForm(instance=g)
		
	return render_to_response('inventar/form.html', {'form': form, 'schein_geraete': schein_geraete, 'back': '/inventar/info/' + str(g.id), 'submit': 'Speichern', 'title': 'Gerät bearbeiten'}, context_instance=RequestContext(request))
