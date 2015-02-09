#coding: utf8 
from Inventar.models import Geraet
from Benutzer.models import Benutzer
from Schein.models import Ausleihschein
from django.shortcuts import render_to_response,redirect
from django.template import RequestContext
#import texcaller
from django.core.servers.basehttp import FileWrapper
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.contrib import messages
from django.db.models import Q
from Schein.forms import ScheinForm
from django.conf import settings

import json
import datetime

@login_required
def erstellen(request):
	benutzer = Benutzer.objects.order_by('nachname', 'vorname')

	if 'u' in request.GET:
		try:
			b = Benutzer.objects.get(pk=int(request.GET['u']))
		except Benutzer.DoesNotExist:
			b = benutzer[0]
	else:
		b = benutzer[0]

	schein_geraete = Geraet.objects.filter(status=Geraet.PENDING)

	return render_to_response('schein/erstellen.html', {'schein_geraete': schein_geraete, 'benutzer': benutzer, 'b': b, 'hideSchein': True}, context_instance=RequestContext(request))

def scheinErstellen(user_id, begin_date, end_date, anderer_abholer, schein_geraete, nummer):
	if anderer_abholer == "1":
		anderer_abholer = True
	else:
		anderer_abholer = False
	b = Benutzer.objects.get(pk=user_id)
	lines = b.anschrift.splitlines()
	anschrift1 = anschrift2 = anschrift3 = ''
	try:
		anschrift1 = lines[0]
		anschrift2 = lines[1]
		anschrift3 = lines[2]
	except IndexError:
		response = 'bla'

	schein_tex = render_to_string('schein/schein.tex', {'nummer': nummer, 'b': b, 'geraete': schein_geraete, 'begin_date': begin_date, 'end_date': end_date, 'anderer_abholer': anderer_abholer, 'anschrift1': anschrift1,'anschrift2': anschrift2,'anschrift3': anschrift3})	

	#f = open(settings.SCHEIN_PATH + "schein.tex", 'w')
	#f.write(schein_tex.encode('utf-8'))
	#f.close()

	pdf, info = texcaller.convert(schein_tex, 'LaTeX', 'PDF', 2)
	return pdf


@login_required
def download(request):
	if "id" in request.GET:
		schein_id = request.GET['id']
		
		filename = 'schein' + str(schein_id) + '.pdf'
		response = HttpResponse(FileWrapper(file(settings.SCHEIN_PATH + filename)), content_type='application/pdf')
		response['Content-Disposition'] = 'attachment; filename=' + filename
		return response

	user = request.user
	user_id = request.GET['u']
	begin_date = datetime.datetime.strptime(request.GET['begindate'], '%d.%m.%Y')
	end_date = datetime.datetime.strptime(request.GET['enddate'], '%d.%m.%Y')

	s, created = Ausleihschein.objects.get_or_create(status=Ausleihschein.PENDING)
	s.issue_user = request.user
	b = Benutzer.objects.get(pk=user_id)
	s.benutzer = b
	s.begin_date = begin_date
	s.end_date = end_date
	
	schein_geraete = Geraet.objects.filter(status=Geraet.PENDING)
	schein_list = []
	for g in schein_geraete:
		schein_list.append(g.id)
	s.geraete = json.dumps(schein_list)
	s.save()
	
	schein_geraete = list(schein_geraete)

	i = 1
	for g in schein_geraete:
		g.order = i
		i += 1

	while len(schein_geraete) < 10:
		schein_geraete.append(Geraet())
	
	pdf = scheinErstellen(user_id, begin_date, end_date, request.GET['abholer'], schein_geraete, s.id)
	file_content = ContentFile(pdf)
	s.schein.save('schein' + str(s.id) + '.pdf', file_content)
	
	response = HttpResponse(pdf, content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename="Schein' + str(s.id) + '.pdf"'
	return response

@login_required
def issue(request):
	s = Ausleihschein.objects.filter(status=Ausleihschein.PENDING)[0]
	s.status = Ausleihschein.BORROWED
	s.save()
	schein_geraete = Geraet.objects.filter(status=Geraet.PENDING)
	
	for g in schein_geraete:
		g.status = Geraet.BORROWED
		g.schein = s
		g.save()

	messages.add_message(request, messages.SUCCESS, 'Der Schein wurde erfolgreich ausgestellt')
	return HttpResponseRedirect('/')

@login_required
def info(request, schein_id):
	schein_geraete = Geraet.objects.filter(status=Geraet.PENDING)
	
	try:
		s = Ausleihschein.objects.get(pk=schein_id)
	except Ausleihschein.DoesNotExist:
		return render_to_response("schein/info_404.html", {'id': schein_id, 'schein_geraete': schein_geraete}, context_instance=RequestContext(request))

	if 'switchStatus' in request.GET:
		if s.status == Ausleihschein.BORROWED:
			s.status = Ausleihschein.RETURNED
			s.return_user = request.user
			getGeraete(s)
			for g in s.geraete_liste:
				g.status = Geraet.AVAILABLE
				g.save()

			messages.add_message(request, messages.SUCCESS, 'Der Schein wurde erfolgreich als zurückgegeben markiert')
		else:
			s.status = Ausleihschein.BORROWED
			messages.add_message(request, messages.SUCCESS, 'Der Schein wurde erfolgreich als ausgeliehen markiert')
		s.save()
		return HttpResponseRedirect('/schein/info/' + schein_id)

	getGeraete(s)
	if s.end_date < datetime.date.today():
			s.late = True

	return render_to_response('schein/info.html', {'s': s,'schein_geraete': schein_geraete}, context_instance=RequestContext(request))
	

@login_required
def index(request):
	scheine_current = Ausleihschein.objects.filter(status=Ausleihschein.BORROWED).order_by('end_date')
	scheine_current = list(scheine_current)

	handle_scheine(scheine_current, True)

	scheine_old = Ausleihschein.objects.filter(status=Ausleihschein.RETURNED).order_by('end_date')
	scheine_old = list(scheine_old)

	handle_scheine(scheine_old, False)
	
	schein_geraete = Geraet.objects.filter(status=Geraet.PENDING)
	return render_to_response("schein/index.html", {'schein_geraete': schein_geraete, 'scheine_current': scheine_current, 'scheine_old': scheine_old}, context_instance=RequestContext(request))

@login_required
def filter_view(request, typ):
	if 's' in request.GET:
		text = request.GET['s']
	else:
		text = ''
	current = True
	if typ == 'current':
		table = 'current'
		status = Ausleihschein.BORROWED
	else:
		current = False
		table = 'old'
		status = Ausleihschein.RETURNED

	s = Ausleihschein.objects.filter(status=status).filter(Q(benutzer__vorname__icontains=text) | Q(benutzer__nachname__icontains=text))
	s = list(s)
	handle_scheine(s, current)
	return render_to_response('schein/table_' + table + '.html', {'scheine_' + table: s}, context_instance=RequestContext(request))

def getGeraete(schein):
	schein.geraete_liste = []
	geraete = json.loads(schein.geraete)
	for g in geraete:
		try:
			geraet = Geraet.objects.get(pk=g)
			schein.geraete_liste.append(geraet)
		except Geraet.DoesNotExist:
			error = "bla"

def handle_scheine(scheine, current):
	for s in scheine:
		getGeraete(s)
		if current and s.end_date < datetime.date.today():
			s.late = True

@login_required
def edit(request, id):
	schein_geraete = Geraet.objects.filter(status=Geraet.PENDING)
	try:
		s = Ausleihschein.objects.get(pk=id)
	except Ausleihschein.DoesNotExist:
		render_to_response('schein/info_404.html', {'schein_geraete': schein_geraete, 'id': id}, context_instance=RequestContext(request))

	if request.method == "POST":
		form = ScheinForm(request.POST, instance=s)
		if form.is_valid():
			s = form.save()
			messages.add_message(request, messages.SUCCESS, 'Der Schein ' + str(s.id) + ' wurde erfolgreich bearbeitet')
			return redirect('/schein/info/' + id)
	else:
		form = ScheinForm(instance=s)

	return render_to_response('schein/form.html', {'form': form, 'schein_geraete': schein_geraete, 'id': id}, context_instance=RequestContext(request))

