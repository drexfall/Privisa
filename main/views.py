from django.shortcuts import render, redirect
from .models import User, PasswordEntry, GeneratorSettings
from .forms import Login, PasswordInput, SettingsForm, Register
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.edit import DeleteView
from .generate import Generator
from django.contrib.auth.hashers import make_password, check_password

# Create your views here.


def register(request, logout=False):
    user = request.user
    form = Register()
    
    if request.method == 'POST':
        form = Register(request.POST)
        if form.is_valid():
            f = form
            # f = form.save(commit=False)
            # f.password = make_password(f.password)
            f.save()
            return HttpResponseRedirect('/vault')

    context = {'title': "Register", 'form': form, "user": user}
    return render(request, 'authenticate.html', context)
def login(request, logout=False):
    user = 'anonymous'
    form = Login()
    
    if request.method == 'POST':
        form = Login(request.POST)
        if form.is_valid():
            if User.objects.filter(username=form.cleaned_data["username"]).exists():
                user = User.objects.get(username=form.cleaned_data["username"])
                
                if form.cleaned_data["password"] == user.password:
                # if check_password(form.cleaned_data["password"], user.password):
                    user.is_authenticated = True
                    user.save()
                    request.user = user
                    return redirect('vault')
                
    context = {'title': "Login", 'form': form, 'user': user}
    return render(request, 'authenticate.html', context)

def logout(request):
    if User.objects.filter(is_authenticated=True).exists():
        user = User.objects.get(is_authenticated=True)
        user.is_authenticated = False
        user.save()
        
        return redirect("home")
    else:
        return redirect("vault")
        

def vault(request):
    if User.objects.filter(is_authenticated=True).exists():
        user = User.objects.get(is_authenticated=True)
    else:
        user = "anonymous"
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

    context = {'title': "Vault", 'user': user, 'userdata': pass_entry_data, "form": form}
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
