from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from Inventar.models import Geraet
from Benutzer.models import Benutzer
from django.db.models import Q
from Benutzer.forms import UserForm
from Inventar.forms import GeraetForm
from django.contrib import messages

@login_required
def index(request):
	schein_geraete = Geraet.objects.filter(status=Geraet.PENDING)
	benutzer = Benutzer.objects.all()

	return render_to_response('benutzer/index.html',{'schein_geraete': schein_geraete, 'benutzer': benutzer}, context_instance=RequestContext(request))

@login_required
def filter_view(request):
	if 's' in request.GET:
		text = request.GET['s']
	else:
		text = ''

	benutzer = Benutzer.objects.filter(Q(vorname__icontains=text) | Q(nachname__icontains=text) | Q(telefon__icontains=text) | Q(anschrift__icontains=text) | Q(status__icontains=text) | Q(raum__icontains=text) | Q(haustel__icontains=text) | Q(kommentar__icontains=text));
	return render_to_response('benutzer/table.html', {'benutzer': benutzer}, context_instance=RequestContext(request))

@login_required
def info(request, id):
	schein_geraete = Geraet.objects.filter(status=Geraet.PENDING)

	try:
		b = Benutzer.objects.get(pk=id)
	except Benutzer.DoesNotExist:
		return render_to_response('benutzer/info_404.html', {'id': id, 'schein_geraete': schein_geraete }, context_instance=RequestContext(request))

	return render_to_response('benutzer/info.html', {'b': b, 'schein_geraete': schein_geraete }, context_instance=RequestContext(request))

@login_required
def get_user(request):
	if request.method == "GET":
		benutzer_id = request.GET['id']
		try:
			b = Benutzer.objects.get(pk=benutzer_id)
		except Benutzer.DoesNotExist:
			return 'error'

		return render_to_response('benutzer/infotable.html', {'b': b}, context_instance=RequestContext(request))

	else:
		return "no GET"


def add(request):
	return "add"

def remove(request):
	return "remove"

@login_required
def create_user(request):
	back = '/schein/erstellen/'
	redirectSchein = True
	if "liste" in request.GET:
		back = '/benutzer/'
		redirectSchein = False
		

	if request.method == "POST":
		form = UserForm(request.POST)
		if form.is_valid():
			user = form.save()
			if redirectSchein:
				return redirect('/schein/erstellen/?u=' + str(user.id))
			else:
				return redirect('/benutzer/')
	else:
		form = UserForm()
	schein_geraete = Geraet.objects.filter(status=Geraet.PENDING)
	return render_to_response('benutzer/form.html', {'form': form, 'schein_geraete': schein_geraete, 'back': back, 'submit': 'Erstellen'}, context_instance=RequestContext(request))


@login_required
def edit(request, id):
	schein_geraete = Geraet.objects.filter(status=Geraet.PENDING)

	try:
		b = Benutzer.objects.get(pk=id)
	except Benutzer.DoesNotExist:
		render_to_response('benutzer/info_404.html', {'schein_geraete': schein_geraete, 'id': id}, context_instance=RequestContext(request))

	if request.method == "POST":
		form = UserForm(request.POST, instance=b)
		if form.is_valid():
			b = form.save()
			messages.add_message(request, messages.SUCCESS, 'Der Benutzer ' + b.vorname + ' ' + b.nachname + ' wurde erfolgreich bearbeitet')
			return redirect('/benutzer/info/' + id)
	else:
		form = UserForm(instance=b)
		
	return render_to_response('benutzer/form.html', {'form': form, 'schein_geraete': schein_geraete, 'back': '/benutzer/info/' + str(b.id), 'submit': 'Speichern', 'title': 'Benutzer bearbeiten'}, context_instance=RequestContext(request))
