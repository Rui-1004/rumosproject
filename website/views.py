from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import User
from .models import Product
from .forms import SignUpForm

def home(request):
    return render(request, 'home.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login concluído!")
            return redirect('home')
        else:
            messages.success(request, "Não foi possível concluir o login.")
            return redirect('login')
    else:
        return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('home')

def signup_user(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			# Authenticate and login
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, "Bem-vindo(a)!")
			return redirect('home')
	else:
		form = SignUpForm()
		return render(request, 'signup.html', {'form':form})

	return render(request, 'signup.html', {'form':form})

def store(request):
    products = Product.objects.all()
    return render(request, 'store.html', {'products' : products})