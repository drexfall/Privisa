from django.shortcuts import render
from .models import User, PasswordEntry, GeneratorSettings
from .forms import Login, PasswordInput, SettingsForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.edit import DeleteView
from .generate import Generator

# Create your views here.


def index(request, logout=False):
    form = Login()
    user = User.objects.all().values()
    if user and user[0]['is_authenticated']:
        return HttpResponseRedirect('/vault')

    if request.method == 'POST':
        form = Login(request.POST)
        if form.is_valid():
            if not user:
                form.save()
                return HttpResponseRedirect('/vault')
            if not user[0]['password']:
                user[0]['password'] = form.cleaned_data['password']

            if form.cleaned_data['password'] == user[0]['password']:
                form.bad_password = False
                user_authen = User.objects.get(id=1)

                user_authen.is_authenticated = True
                user_authen.save()
                return HttpResponseRedirect('/vault')
            else:
                form.bad_password = True
                user_authen = User.objects.get(id=1)
                user_authen.is_authenticated = False
                user_authen.save()
    context = {'title': "Login", 'form': form, 'user': user[0] if user else []}
    return render(request, 'index.html', context)


def logout(request):
    if not User.objects.all():
        User(password="", is_authenticated=False).save()
    user_authen = User.objects.get(id=1)
    user_authen.is_authenticated = False
    user_authen.save()
    return HttpResponseRedirect('/')


def vault(request):
    user_data = User.objects.all().values()
    pass_entry_data = PasswordEntry.objects.all().values()

    if request.method == 'POST':
        form = PasswordInput(request.POST)
        if form.is_valid():
            website = form.cleaned_data['website']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            pass_entry = PasswordEntry(
                website=website, username=username, password=password)
            pass_entry.save()

    else:
        form = PasswordInput()

    context = {'title': "Vault", 'user': user_data[0] if user_data else [
    ], 'userdata': pass_entry_data, "form": form}
    return render(request, 'vault.html', context)


def generator(request):
    user_data = User.objects.all().values()
    if not GeneratorSettings.objects.all():
        GeneratorSettings(digits=False,
                          alphabets=True,
                          punctuations=False,
                          uppercase=False,
                          length=8).save()

    settings = GeneratorSettings.objects.get(id=1)

    if request.method == 'POST':
        settings.digits = request.POST.get('digits', '') == 'on'
        settings.alphabets = request.POST.get('alphabets', '') == 'on'
        settings.punctuations = request.POST.get('punctuations', '') == 'on'
        settings.uppercase = request.POST.get('uppercase', '') == 'on'

        if (request.POST.get('length', '')):
            settings.length = request.POST.get('length')

        settings.save()
    generator_obj = Generator()
    generator_obj.generate()

    form = SettingsForm()

    context = {'title': "Generator",
               'password': generator_obj.password, 'form': form, 'user': user_data[0] if user_data else [],}
    return render(request, 'generator.html', context)


def vault_delete(request, id):
    obj = PasswordEntry.objects.get(id=id)
    obj.delete()
    return HttpResponseRedirect(reverse('vault'))


def vault_update(request, id, username, password):
    obj = PasswordEntry.objects.get(id=id)
    obj.username = username
    obj.password = password
    obj.save()
    return HttpResponseRedirect(reverse('vault'))
